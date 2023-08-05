"""
sms http sdk
"""

from smssdk.https.auth.auth import get_token
from smssdk.https.requests.api_request import request_for_batch_sms, request_for_p2p_sms
from smssdk.utils.exceptions import SMSServiceException
from smssdk.utils.values import REGEX, URLS
import re


class HttpTool:
    def __init__(self, account: str, password: str, server_name: str, protocol: str):
        """
        :param account: 客户账号
        :param password: 客户账号密码
        :param server_name: http服务地址，一般来说是个域名
        :param protocol: 协议。http/https
        """
        if not account or type(account) is not str or str.strip(account) == '':
            raise SMSServiceException(f'[https.__init__.py:HttpTool.__init__()]入参account有误，account:{account}')
        if not password or type(password) is not str or str.strip(password) == '':
            raise SMSServiceException(f'[https.__init__.py:HttpTool.__init__()]入参password有误，password:{password}')
        if not server_name or type(server_name) is not str or str.strip(server_name) == '':
            raise SMSServiceException(
                f'[https.__init__.py:HttpTool.__init__()]入参server_name有误，server_name:{server_name}')
        if not protocol or type(protocol) is not str or protocol not in ['http', 'https']:
            raise SMSServiceException(f'[https.__init__.py:HttpTool.__init__()]入参protocol有误，protocol:{protocol}')
        self._account = account
        self._password = password
        self._token_url = protocol + '://' + server_name + URLS['TOKEN']
        self._batch_send_url = protocol + '://' + server_name + URLS['BATCH_SMS']
        self._p2p_send_url = protocol + '://' + server_name + URLS['P2P_SMS']

    def http_batch_sms(self, phone_numbers: list, message_content: str, access_number: str = None):
        """
        调用此函数发起sms批量短信发送服务
        zgl/2022.09.08
        :param phone_numbers: 目标手机号
        :param message_content: 短信内容
        :param access_number: 虚拟接入码。非必填
        :return: 短信发送记录，[{'phoneNumber': str, 'msgId': str, 'code': int}, ...]
        """
        # 入参校验
        if not phone_numbers or type(phone_numbers) is not list:
            raise SMSServiceException(
                f'[https.__init__.py:HttpTool.http_batch_sms()]入参phone_numbers有误，phone_numbers:{phone_numbers}')
        else:
            for x in phone_numbers:
                if not x or type(x) is not str or str.strip(x) == '' or not re.search(REGEX['MOBILE_PHONE'], x):
                    raise SMSServiceException(f"[HttpTool:http_batch_sms]phone_numbers存在某元素有误, phoneNumber:{x}")
        if not message_content or type(message_content) is not str or str.strip(message_content) == '':
            raise SMSServiceException(f'[https.__init__.py:HttpTool.http_batch_sms()]入参message_content有误，'
                                      f'message_content:{message_content}')
        # 获取token
        token = get_token(self._token_url, self._account, self._password)
        # 调用api
        return request_for_batch_sms(self._batch_send_url, token, phone_numbers, message_content, access_number)

    def http_p2p_sms(self, params_list: list):
        """
        调用此函数发起sms点对点短信发送服务
        zgl/2022.09.08
        :param params_list: sms参数列表，结构如下：
            [
                {
                    'phoneNumber': str,
                    'messageContent': str,
                    'bizId': str,
                    'accessNumber': str
                },
                ...
            ]
        :return: 短信发送记录，[{'phoneNumber': str, 'msgId': str, 'code': int}, ...]
        """
        # 入参校验
        if not params_list or type(params_list) is not list:
            raise SMSServiceException(
                f'[https.__init__.py:HttpTool.http_p2p_sms()]params_list有误，params_list:{params_list}')
        else:
            for x in params_list:
                if not x['phoneNumber'] or type(x['phoneNumber']) is not str or str.strip(x['phoneNumber']) == '' \
                        or not re.search(REGEX['MOBILE_PHONE'], x['phoneNumber']):
                    raise SMSServiceException(
                        f"[https.__init__.py:HttpTool.http_p2p_sms()]params_list存在某元素的phoneNumber有误, "
                        f"phoneNumber:{x['phoneNumber']}")
                if not x['messageContent'] or type(x['messageContent']) is not str or str.strip(
                        x['messageContent']) == '':
                    raise SMSServiceException(
                        f"[https.__init__.py:HttpTool.http_p2p_sms()]params_list存在某元素的messageContent有误, "
                        f"messageContent:{x['messageContent']}")
        # 获取token
        token = get_token(self._token_url, self._account, self._password)
        # 调用api
        return request_for_p2p_sms(self._p2p_send_url, token, params_list)
