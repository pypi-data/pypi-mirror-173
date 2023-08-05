"""
SP->ISMG连接请求参数封装
"""
import hashlib
import struct
import time
from smssdk.utils.values import CMPP_COMMAND_ID, CMPP_VERSION

from smssdk.tcp.cmpp.reqdata import RequestData


class ConnectReq(RequestData):
    def __init__(self, sp_id, sp_secret, version: int):
        """
        封装SP->ISMG连接请求的消息体
        :version: CMPP版本。2/3
        """
        # 源地址Source_Addr。6字节。
        _sp_id = sp_id.encode('utf-8')
        # SP公钥。16字节。
        _sp_secret = sp_secret.encode("utf-8")
        # CMPP协议版本号Version（!B：格式为integer，存储时按大端排列；0x20：0010 0000）。1字节。
        if version == CMPP_VERSION['TWO']:
            _version = struct.pack('!B', 0x20)
        else:
            _version = struct.pack('!B', 0x30)
        _time_str = time.strftime('%m%d%H%M%S', time.localtime(time.time()))
        # 时间戳Timestamp（!L：格式为long，存储时按大端排列）。4字节。
        _timestamp = struct.pack('!L', int(_time_str))

        # 封装鉴别源地址AuthenticatorSource。（b'\x00'：0的字节类型）
        # 加密规则：MD5（Source_Addr + 9字节的0 + shared secret + timestamp）。timestamp格式：MMDDHHMMSS，即月日时分秒，10位。
        self.authenticator_source = hashlib.md5(_sp_id + 9 * b'\x00' + _sp_secret + _time_str.encode('utf-8')).digest()

        # 组装消息体
        message_body = _sp_id + self.authenticator_source + _version + _timestamp

        # 组装最终消息=消息头+消息体
        RequestData.__init__(self, CMPP_COMMAND_ID['CMPP_CONNECT'], message_body)
