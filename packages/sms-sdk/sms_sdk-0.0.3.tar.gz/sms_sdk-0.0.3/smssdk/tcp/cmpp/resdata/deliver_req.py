"""
解析ISMG->SP发送消息事件中ISMG的请求消息
"""
import struct

from smssdk.tcp.cmpp.resdata import ResponseData
from smssdk.utils.logger import Logger
from smssdk.utils.values import CMPP_REGISTERED_DELIVERY, CMPP_VERSION

logger = Logger('tcp.cmpp.resdata.deliver_req.py')


class DeliverReq(ResponseData):
    def __init__(self, message, version: int):
        # logger.info(f'[DeliverReq.__init__()]收到ISMG网关发送的消息，内容：{message.hex()}。')

        # 解析出消息头和消息体
        ResponseData.__init__(self, message)
        message_body = self.message_body

        # v2和v3不同解析
        if version == CMPP_VERSION['TWO']:
            # Registered_Delivery。长度1字节，无符号整数
            self.registered_delivery, = struct.unpack('!B', message_body[63:64])
            # 判断是不是状态报告，是的话解析状态报告（msg_content）
            if self.registered_delivery == CMPP_REGISTERED_DELIVERY['IS_REPORT']:
                self.is_report = True
                self.raw_report = message_body[65:125]
                self.callback_res = {
                    'msg_id': struct.unpack('!Q', self.raw_report[0:8])[0],
                    'stat': self.raw_report[8:15].decode('utf-8'),
                    'submit_time': self.raw_report[15:25].decode('utf-8'),
                    'done_time': self.raw_report[25:35].decode('utf-8'),
                    'dest_terminal_id': self.raw_report[35:56].decode('utf-8'),
                    'smsc_sequence': struct.unpack('!L', self.raw_report[56:])[0]
                }
                self.msg_id = self.callback_res['msg_id']
            else:
                self.is_report = False
        else:
            # Registered_Delivery。长度1字节，无符号整数
            self.registered_delivery, = struct.unpack('!B', message_body[75:76])
            # 判断是不是状态报告，是的话解析状态报告（msg_content）
            if self.registered_delivery == CMPP_REGISTERED_DELIVERY['IS_REPORT']:
                self.is_report = True
                self.raw_report = message_body[77:148]
                self.callback_res = {
                    'msg_id': struct.unpack('!Q', self.raw_report[0:8])[0],
                    'stat': self.raw_report[8:15].decode('utf-8'),
                    'submit_time': self.raw_report[15:25].decode('utf-8'),
                    'done_time': self.raw_report[25:35].decode('utf-8'),
                    'dest_terminal_id': self.raw_report[35:67].decode('utf-8'),
                    'smsc_sequence': struct.unpack('!L', self.raw_report[67:])[0]
                }
                self.msg_id = self.callback_res['msg_id']
            else:
                self.is_report = False
