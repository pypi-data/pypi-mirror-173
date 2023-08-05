"""
解析ISMG网关响应入口
"""
import struct


class ResponseData:
    def __init__(self, message):
        self.length, = struct.unpack('!L', message[0:4])
        self.command_id, = struct.unpack('!L', message[4:8])
        self.sequence, = struct.unpack('!L', message[8:12])
        self.message_body = message[12:self.length]
