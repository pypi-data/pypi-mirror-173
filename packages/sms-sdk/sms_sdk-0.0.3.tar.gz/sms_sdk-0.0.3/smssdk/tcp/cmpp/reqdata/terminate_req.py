"""
SP->ISMG断开连接参数封装
"""

from smssdk.tcp.cmpp.reqdata import RequestData
from smssdk.utils.values import CMPP_COMMAND_ID


class TerminateReq(RequestData):
    def __init__(self):
        # 拆除ISMG连接无消息体
        message_body = b''
        RequestData.__init__(self, CMPP_COMMAND_ID['CMPP_TERMINATE'], message_body)
