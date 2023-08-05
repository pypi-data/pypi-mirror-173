"""
解析SP->ISMG发送消息事件中ISMG响应的消息体
"""

import struct
from smssdk.tcp.cmpp.resdata import ResponseData
from smssdk.utils.logger import Logger
from smssdk.utils.values import CMPP_VERSION

logger = Logger('tcp.cmpp.resdata.submit_res.py')


class SubmitRes(ResponseData):
    def __init__(self, message, version: int):
        """
        :param version: CMPP版本。2/3
        """
        # logger.info(f'[SubmitRes.__init__()]收到向ISMG网关发送消息的响应，消息参数：{message.hex()}。')

        # 解析出消息头和消息体
        ResponseData.__init__(self, message)
        message_body = self.message_body

        # 解析消息体
        # Msg_Id
        self.msg_id, = struct.unpack('!Q', message_body[0:8])
        # Result。v2长度为1，v3长度为4
        if version == CMPP_VERSION['TWO']:
            self.result, = struct.unpack('!B', message_body[8:])
        else:
            self.result, = struct.unpack('!L', message_body[8:])

        self.callback_res = {
            'msg_id': self.msg_id,
            'result': self.result
        }
