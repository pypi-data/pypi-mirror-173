"""
解析ISMG->SP激活测试
"""
from smssdk.tcp.cmpp.resdata import ResponseData
from smssdk.utils.logger import Logger

logger = Logger('tcp.cmpp.resdata.active_res.py')


class ActiveReq(ResponseData):
    def __init__(self, message):
        # logger.info(f'[ActiveRes.__init__()]收到心跳，消息参数：{message.hex()}。')

        # 是心跳
        # self.is_active_test = True

        # 无消息体
        ResponseData.__init__(self, message)
