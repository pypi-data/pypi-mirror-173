"""
封装tcp请求数据
"""

import struct
from smssdk.utils.values import NUMBERS

# 消息流水号,顺序累加,步长为1
_global_seq_no = NUMBERS['ZERO']


class RequestData:
    def __init__(self, command_id, message_body):
        """
        :param command_id: CMPP命令代码，如0x00000001
        :param message_body: 这次请求的消息体
        """
        self._command_id = command_id
        self._message_body = message_body

        global _global_seq_no
        # 步长为1
        _global_seq_no += NUMBERS['ONE']
        self.sequence = _global_seq_no

        # 拼接最终请求参数(消息头+消息体)。!L:long型格式，存储时按大端排序
        # 格式：消息头(消息总长度(含该值的长度)+命令id+消息流水号) + 消息体
        # 对应长度：12(4+4+4) + len(消息体)
        self.message = struct.pack('!L', 12 + len(self._message_body)) \
                       + struct.pack('!L', self._command_id) \
                       + struct.pack('!L', self.sequence) \
                       + self._message_body
