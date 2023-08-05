"""
解析SP->ISMG连接请求中ISMG响应的消息体
"""
import struct

from . import ResponseData
from smssdk.utils.logger import Logger

logger = Logger('tcp.cmpp.resdata.connect_res.py')


class ConnectRes(ResponseData):
    def __init__(self, message):
        # logger.info(f'[ConnectRes.__init__()]收到连接ISMG网关的响应，消息参数：{message.hex()}')

        # 解析出消息头和消息体
        ResponseData.__init__(self, message)
        message_body = self.message_body

        # 解析消息体
        # 状态Status
        self.status, = struct.unpack('!B', message_body[0:1])
        # ISMG认证码AuthenticatorISMG，用于鉴别ISMG
        self.raw_authenticator_ISMG = message_body[1:17]
        # 服务器支持的最高版本号Version
        self.version, = struct.unpack('!B', message_body[17:])

        # 回调dict
        self.callback_res = {
            'status': self.status,
            'authenticator_ISMG': self.raw_authenticator_ISMG.hex(),
            'version': self.version,
        }
