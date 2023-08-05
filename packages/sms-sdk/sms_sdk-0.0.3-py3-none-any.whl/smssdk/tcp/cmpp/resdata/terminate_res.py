"""
解析SP->ISMG断开连接请求中ISMG响应的消息体
"""
from smssdk.tcp.cmpp.resdata import ResponseData
from smssdk.utils.logger import Logger

logger = Logger('tcp.cmpp.resdata.terminate_res.py')


class TerminateRes(ResponseData):
    def __init__(self, message):
        # logger.info(f'[TerminateRes.__init__()]收到断开ISMG网关连接的响应，消息参数：{message.hex()}。')

        # 拆除ISMG连接响应无消息体
        ResponseData.__init__(self, message)
