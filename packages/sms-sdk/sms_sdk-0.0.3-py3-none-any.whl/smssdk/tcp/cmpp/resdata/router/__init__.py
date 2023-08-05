"""
ISMG响应解析函数路由
"""
import struct

from smssdk.tcp.cmpp.resdata.connect_res import ConnectRes
from smssdk.tcp.cmpp.resdata.deliver_req import DeliverReq
from smssdk.tcp.cmpp.resdata.submit_res import SubmitRes
from smssdk.tcp.cmpp.resdata.terminate_res import TerminateRes
from smssdk.tcp.cmpp.resdata.active_req import ActiveReq
from smssdk.utils.values import CMPP_COMMAND_ID

# 不需要根据cmpp版本区分的解析函数
_res_mapping_common = {
    CMPP_COMMAND_ID['CMPP_CONNECT_RESP']: ConnectRes
    , CMPP_COMMAND_ID['CMPP_TERMINATE_RESP']: TerminateRes
    , CMPP_COMMAND_ID['CMPP_ACTIVE_TEST']: ActiveReq
}

# 需要根据cmpp版本区分的解析函数
_res_mapping_diff_by_version = {
    CMPP_COMMAND_ID['CMPP_SUBMIT_RESP']: SubmitRes
    , CMPP_COMMAND_ID['CMPP_DELIVER']: DeliverReq
}


def parse_response(message, version: int):
    """
    路由具体的解析函数
    :param message: 原生的ISMG响应
    :param version: CMPP版本
    :return:
    """
    command_id, = struct.unpack('!L', message[4:8])
    if command_id in _res_mapping_common.keys():
        return _res_mapping_common[command_id](message)
    elif command_id in _res_mapping_diff_by_version.keys():
        return _res_mapping_diff_by_version[command_id](message, version)
