import logging
import random
from datetime import datetime

import pytz
import requests
import time

from django.forms import model_to_dict
from django.utils import timezone

from xj_finance.services.finance_service import FinanceService
from xj_finance.services.finance_transact_service import FinanceTransactService
from xj_enroll.service.enroll_services import EnrollServices
from xj_thread.services.thread_item_service import ThreadItemService
from xj_user.services.user_service import UserService
from xj_payment.models import PaymentPayment
from xj_user.services.user_sso_serve_service import UserSsoServeService
from ..services.payment_wechat_service import PaymentWechatService


class PaymentService:
    @staticmethod
    def pay(params):
        # print(params)
        data = params
        data['total_fee'] = float(params['total_amount']) * 100  # 元转分
        payment_data = None
        out_trade_no = timezone.now().strftime('%Y%m%d%H%M%S') + ''.join(
            map(str, random.sample(range(0, 9), 4)))  # 随机生成订单号
        params['out_trade_no'] = out_trade_no
        if params['enroll_id']:
            enroll_data, err_txt = EnrollServices.enroll_detail(params['enroll_id'])  # 判断是否是报名订单
            if err_txt:
                return "报名记录不存在"
            data['enroll_id'] = enroll_data['id']
            data['user_id'] = enroll_data['user_id']
        # 单点登录信息
        sso_data, err = UserSsoServeService.user_sso_to_user(data['user_id'])
        if err:
            return "单点登录记录不存在"
        sso_data = model_to_dict(sso_data)
        data['openid'] = sso_data['sso_unicode']
        tz = pytz.timezone('Asia/Shanghai')
        # 返回时间格式的字符串
        # now_time = timezone.now().astimezone(tz=tz)
        # now_time_str = now_time.strftime("%Y.%m.%d %H:%M:%S")
        # 返回datetime格式的时间
        now_time = timezone.now().astimezone(tz=tz).strftime("%Y-%m-%d %H:%M:%S")
        now = datetime.strptime(now_time, '%Y-%m-%d %H:%M:%S')
        payment_data = {
            "order_no": out_trade_no,
            "enroll_id": data['enroll_id'],
            "user_id": data['user_id'],
            "total_amount": int(data['total_fee']),
            "create_time": now,
        }
        data['platform'] = 'muzpay'
        data['currency'] = 'CNY'

        PaymentPayment.objects.create(**payment_data)
        # 支付方式检查
        if params['payment_method'] == "applets":  # 微信小程序支付

            payment = PaymentWechatService.payment_applets_pay(data)

        elif params['payment_method'] == "balance":  # 余额支付
            payment = PaymentWechatService.payment_balance_pay(data)

        return payment

        # 支付逻辑处理

    @staticmethod
    def payment_logic_processing(param):
        try:
            project_name = None
            summary = None
            out_trade_no = param['out_trade_no']  # 订单号
            total_fee = param['total_fee']  # 金额（单位分）
            transaction_id = param['transaction_id']  # 微信支付订单号
            finance_data = {
                "order_no": out_trade_no,
                "transact_id": transaction_id,
                "their_account_id": "1",
                "platform": "muzpay",
                "amount": total_fee,
                "currency": "CNY",
                "pay_mode": "WECHAT",
            }
            # 根据订单号查询支付记录是否存在
            payment = PaymentPayment.objects.filter(order_no=int(out_trade_no)).first()
            if not payment:
                logging.info("payment_callback" + "订单不存在")
            payment_message = model_to_dict(payment)
            finance_data['account_id'] = payment_message['user_id']
            finance_data['enroll_id'] = payment_message['enroll_id']
            # 根据支付记录用户 查询用户基本信息
            user_set, err = UserService.user_basic_message(payment_message['user_id'])
            if user_set:
                if payment_message['enroll_id']:
                    # 如果存在报名id 查询报名记录
                    enroll_set, err = EnrollServices.enroll_detail(payment_message['enroll_id'])
                    if enroll_set:
                        # 报名表支付状态修改
                        enroll_data = {
                            "enroll_status_code": "422",
                            "paid_amount": total_fee
                        }
                        enroll_data, enroll_err_txt = EnrollServices.enroll_edit(enroll_data,
                                                                                 payment_message['enroll_id'])
                        if enroll_err_txt:
                            logging.info("payment_callback_enroll" + enroll_err_txt)
                        # 根据报名记录获取 信息模块项目基本信息
                        thread_set, err = ThreadItemService.detail(enroll_set['thread_id'])
                        if thread_set:
                            project_name = thread_set['title']
                summary = "【" + user_set['full_name'] + "】支付 【" + project_name + "】款项"
            finance_data['summary'] = summary
            # # TODO 拿到订单号后的操作 看自己的业务需求
            funance_add_data, err_txt = FinanceTransactService.post(finance_data)
            if err_txt:
                logging.info("payment_callback" + err_txt)
            # 根据唯一交易id 查询主键id
            funance_data, err = FinanceTransactService.finance_transact_detailed(transaction_id)
            if funance_data:
                funance_data = model_to_dict(funance_data)
                payment_data = {
                    "transact_no": transaction_id,
                    "transact_id": funance_data['id'],
                    "order_status_id": "24"
                }
                # 更改支付记录
                PaymentPayment.objects.filter(order_no=int(out_trade_no)).update(**payment_data)
        except Exception as e:
            print(e)
            logging.info("payment_logic_processing" + e)
