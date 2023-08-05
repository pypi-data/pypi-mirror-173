"""
SP->ISMG信息发送参数封装
"""

import struct
from smssdk.tcp.cmpp.reqdata import RequestData
from smssdk.utils.exceptions import SMSServiceException
from smssdk.utils.values import CMPP_COMMAND_ID, CMPP_VERSION


class SubmitReq(RequestData):
    def __init__(self,
                 version: int,
                 msg_src,
                 msg_content: str,
                 src_id: str,
                 dest_terminal_id: list = None,
                 pk_total=1,
                 pk_number=1,
                 registered_delivery: int = 1,
                 msg_level=0,
                 service_id='MI',
                 fee_usertype=2,
                 fee_terminal_id="",
                 tp_pid=0,
                 tp_udhi=0,
                 msg_fmt=8,
                 feetype='01',
                 feecode='103013',
                 valid_time=17 * '\x00',
                 at_time=17 * '\x00',
                 reserve='',
                 fee_terminal_type=0,
                 dest_terminal_type=0,
                 link_id=20 * '\x00',
                 split_send=False,
                 content_prefix: bytes = ''):
        """
        构建SP->ISMG发送消息事件的消息体
        :param version: cmpp协议版本，2/3
        :param msg_src: 即spId，由客户传入
        :param msg_content: 消息内容，客户传入
        :param src_id: 接入码。由客户传入
        :param dest_terminal_id: 接收短信的号码
        :param pk_total:
        :param pk_number:
        :param registered_delivery: 是否需要返回状态报告
        :param msg_level:
        :param service_id:
        :param fee_usertype:
        :param fee_terminal_id:
        :param tp_pid:
        :param tp_udhi:
        :param msg_fmt:
        :param feetype:
        :param feecode:
        :param valid_time:
        :param at_time:
        :param reserve: v2独有参数：保留。
        :param fee_terminal_type: v3独有参数：被计费用户的号码类型，0：真实号码；1：伪码。
        :param dest_terminal_type: v3独有参数：接收短信的用户的号码类型，0：真实号码；1：伪码。
        :param link_id: v3独有参数：点播业务使用的LinkID，非点播类业务的MT流程不使用该字段。
        :param split_send: 是否做了长短信拆分。True/False
        :param content_prefix: 长短信拆分后，要加在content前面的标志。
        """

        # 信息标识Msg_Id，由SP侧短信网关本身产生，本处填空。8字节。
        _msg_id = 8 * b'\x00'
        # 相同Msg_Id的信息总条数Pk_total，从1开始。1字节。
        _pk_total = struct.pack('!B', pk_total)
        # 相同Msg_Id的信息序号Pk_number，从1开始。1字节。
        _pk_number = struct.pack('!B', pk_number)
        # 是否要求返回状态确认报告Registered_Delivery，0：不需要；1：需要；2：产生SMC话单。
        _registered_delivery = struct.pack('!B', registered_delivery)
        # 信息级别Msg_level。1字节。
        _msg_level = struct.pack('!B', msg_level)
        # 业务类型Service_Id，是数字、字母和符号的组合。10字节。
        _service_id = (service_id + (10 - len(service_id)) * '\x00').encode('utf-8')
        # 计费用户类型字段Fee_UserType，1字节。
        # 0：对目的终端MSISDN计费
        # 1：对源终端MSISDN计费
        # 2：对SP计费
        # 3：表示本字段无效，对谁计费参见Fee_terminal_Id字段
        _fee_usertype = struct.pack('!B', fee_usertype)
        # 被计费用户的号码Fee_terminal_Id（如本字节填空，则表示本字段无效，对谁计费参见Fee_UserType字段，本字段与Fee_UserType字段互斥）。v2:21字节，v3:32字节
        if version == CMPP_VERSION['TWO']:
            _fee_terminal_id = (fee_terminal_id + (21 - len(fee_terminal_id)) * '\x00').encode('utf-8')
        else:
            _fee_terminal_id = (fee_terminal_id + (32 - len(fee_terminal_id)) * '\x00').encode('utf-8')
            # v3独有参数：被计费用户的号码类型，0：真实号码；1：伪码。1字节无符号整数
            self._fee_terminal_type = struct.pack('!B', fee_terminal_type)
        # GSM协议类型TP_pId。1字节。
        _tp_pid = struct.pack('!B', tp_pid)
        # GSM协议类型TP_udhi。1字节。长短信拆分时为1，普通为0
        if split_send:
            tp_udhi = 1
        _tp_udhi = struct.pack('!B', tp_udhi)
        # 信息格式Msg_Fmt。1字节。
        # 0：ASCII串
        # 3：短信写卡操作
        # 4：二进制信息
        # 8：UCS2编码
        # 15：含GB汉字
        _msg_fmt = struct.pack('!B', msg_fmt)
        # 信息内容来源(SP_Id)Msg_src。6字节。
        _msg_src = msg_src.encode('utf-8')
        # 资费类别FeeType。2字节。
        # 01：对“计费用户号码”免费
        # 02：对“计费用户号码”按条计信息费
        # 03：对“计费用户号码”按包月收取信息费
        # 04：对“计费用户号码”的信息费封顶
        # 05：对“计费用户号码”的收费是由SP实现
        _feetype = feetype.encode('utf-8')
        # 资费代码（以分为单位）FeeCode。6字节。
        _feecode = feecode.encode('utf-8')
        # 存活有效期ValId_Time。17字节。
        _valid_time = valid_time.encode('utf-8')
        # 定时发送时间At_Time。17字节。
        _at_time = at_time.encode('utf-8')
        # 源号码Src_Id。21字节。
        # SP的服务代码或前缀为服务代码的长号码, 网关将该号码完整的填到SMPP协议Submit_SM消息相应的source_addr字段，该号码最终在用户手机上显示为短消息的主叫号码。
        _src_id = (src_id + (21 - len(src_id)) * '\x00').encode('utf-8')
        # 接收信息的用户数量(小于100个用户)DestUsr_tl。1字节。
        _destusr_tl = struct.pack('!B', len(dest_terminal_id))
        # 接收短信的MSISDN号码Dest_terminal_Id。长度21*DestUsr_tl。
        _dest_terminal_id = b""
        if version == CMPP_VERSION['TWO']:
            for msisdn in dest_terminal_id:
                _dest_terminal_id += (msisdn + (21 - len(msisdn)) * '\x00').encode('utf-8')
        else:
            for msisdn in dest_terminal_id:
                _dest_terminal_id += (msisdn + (32 - len(msisdn)) * '\x00').encode('utf-8')
            # v3独有参数：接收短信的用户的号码类型，0：真实号码；1：伪码。1字节无符号整数
            self._dest_terminal_type = struct.pack('!B', dest_terminal_type)
        # 信息内容Msg_Content。长度不固定。
        if split_send:
            _msg_content = content_prefix + msg_content.encode('utf-16-be')
        else:
            _msg_content = msg_content.encode('utf-16-be')
        # 信息长度(Msg_Fmt值为0时：<160个字节；其它<=140个字节)Msg_Length。1字节。
        _msg_length = struct.pack('!B', len(_msg_content))
        if version == CMPP_VERSION['TWO']:
            # v2独有参数：保留Reserve。8字节。
            self._reserve = (reserve + (8 - len(reserve)) * '\x00').encode('utf-8')
        else:
            # v3独有参数：点播业务使用的LinkID，非点播类业务的MT流程不使用该字段。长度20的十六进制字节序列。
            self._link_id = (link_id + (20 - len(link_id)) * '\x00').encode('utf-8')

        # print(_msg_id.hex())
        # print(_pk_total.hex())
        # print(_pk_number.hex())
        # print(_registered_delivery.hex())
        # print(_service_id.hex())
        # print(_fee_usertype.hex())
        # print(_fee_terminal_id.hex())
        # print(_tp_pid.hex())
        # print(_tp_udhi.hex())
        # print(_msg_fmt.hex())
        # print(_msg_src.hex())
        # print(_feetype.hex())
        # print(_feecode.hex())
        # print(_valid_time.hex())
        # print(_at_time.hex())
        # print(_src_id.hex())
        # print(_destusr_tl.hex())
        # print(_dest_terminal_id.hex())
        # print(_msg_length.hex())
        # print(_msg_content.hex())
        # print(_reserve.hex())
        # 组装消息体
        _message_body = ''
        if version == CMPP_VERSION['TWO']:
            _message_body = _msg_id + \
                            _pk_total + _pk_number + \
                            _registered_delivery + \
                            _msg_level + \
                            _service_id + \
                            _fee_usertype + _fee_terminal_id + \
                            _tp_pid + _tp_udhi + \
                            _msg_fmt + _msg_src + \
                            _feetype + _feecode + \
                            _valid_time + _at_time + \
                            _src_id + _destusr_tl + \
                            _dest_terminal_id + \
                            _msg_length + \
                            _msg_content + \
                            self._reserve
        else:
            _message_body = _msg_id + \
                            _pk_total + _pk_number + \
                            _registered_delivery + \
                            _msg_level + \
                            _service_id + \
                            _fee_usertype + _fee_terminal_id + \
                            self._fee_terminal_type + \
                            _tp_pid + _tp_udhi + \
                            _msg_fmt + _msg_src + \
                            _feetype + _feecode + \
                            _valid_time + _at_time + \
                            _src_id + _destusr_tl + \
                            _dest_terminal_id + self._dest_terminal_type + \
                            _msg_length + \
                            _msg_content + \
                            self._link_id

        RequestData.__init__(self, CMPP_COMMAND_ID['CMPP_SUBMIT'], _message_body)
