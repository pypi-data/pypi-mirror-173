"""
sms tcp cmpp sdk
"""
import hashlib
import re
import struct
import time

from smssdk.tcp.cmpp.reqdata import connect_req, submit_req, terminate_req
from smssdk.utils.logger import Logger
from smssdk.utils.exceptions import SMSServiceException
from smssdk.utils.values import NUMBERS, REGEX, CMPP_VERSION, MESSAGE_SPLIT_MARK_PREFIX
from .callback import BasicCallback
from .sockettool import Socket
from smssdk.utils.mythread import Thread

logger = Logger('tcp.cmpp.__init__.py')


class CmppTool:
    def __init__(self, version: int, host: str, port: int, sp_id: str, sp_secret: str, access_number: str,
                 callback_imp: BasicCallback = None):
        """
        :param version: 版本。2/3
        :param host: 服务地址
        :param port: 端口。0~65535
        :param sp_id: 客户spId
        :param sp_secret: sp公钥
        :param access_number: 接入码
        :param callback_imp: 回调类，继承BasicCallback并重写方法
        """
        if version not in CMPP_VERSION.values():
            raise SMSServiceException(f'[tcp.cmpp.__init__.py:CmppTool.__init__()]入参version有误，仅可为2或3')
        # 3.0暂时不可用
        if version == CMPP_VERSION['THREE']:
            raise SMSServiceException(f'[tcp.cmpp.__init__.py:CmppTool.__init__()]version3.0暂不可用，请用2.0版本')
        if not host or type(host) is not str or str.strip(host) == '':
            raise SMSServiceException(f'[tcp.cmpp.__init__.py:CmppTool.__init__()]入参host有误，host:{host}')
        if not port or type(port) is not int or port < NUMBERS['ONE'] or port > NUMBERS['MAX_PORT']:
            raise SMSServiceException(f'[tcp.cmpp.__init__.py:CmppTool:__init__()]入参port有误，port:{port}')
        if not sp_id or type(sp_id) is not str or str.strip(sp_id) == '':
            raise SMSServiceException(f'[tcp.cmpp.__init__.py:CmppTool:__init__()]入参sp_id有误，sp_id:{sp_id}')
        if not sp_secret or type(sp_secret) is not str or str.strip(sp_secret) == '':
            raise SMSServiceException(
                f'[tcp.cmpp.__init__.py:CmppTool:__init__()]入参sp_secret有误，sp_secret:{sp_secret}')
        if not access_number or type(access_number) is not str or str.strip(access_number) == '':
            raise SMSServiceException(
                f'[tcp.cmpp.__init__.py:CmppTool:__init__()]入参access_number有误，access_number:{access_number}')

        self._cmpp_version = version
        self._sp_id = sp_id
        self._sp_secret = sp_secret
        self._access_number = access_number
        self._callback = callback_imp
        if not self._callback:
            self._callback = BasicCallback()

        # 记录长短信拆分操作次数，作为该操作的唯一序号
        self._msg_split_key = NUMBERS['ZERO']

        # 初始化socket
        self._so = Socket(cmpp_version=self._cmpp_version, host=host, port=port, callback=self._callback)

    def connect_ismg(self):
        """
        连接ISMG，创建通道
        :return: bool。True：创建成功
        """
        # socket连接是否已在线
        if self._so.is_online():
            logger.info(
                f"[CmppTool.connect_ismg()][v{self._cmpp_version}]"
                f"连接socket服务端时检测到原有连接，将使用原有连接。")
            return
        # 连接socket
        self._so.connect_socket()
        # 启用子线程持续监听服务端发送的消息。函数作为参数时，不要写()，此处为read而非read()
        Thread(target=self._so.read).start()
        # SP->ISMG连接的请求参数
        connect_req_params = connect_req.ConnectReq(self._sp_id, self._sp_secret, version=self._cmpp_version)
        # 发出SP-ISMG的连接请求
        self._so.write(connect_req_params.message, event='connect_imsg')

    def terminate_ismg(self):
        """
        断开与ISMG的连接
        """
        # socket连接是否还在线
        if not self._so.is_online():
            raise SMSServiceException(f'[tcp.cmpp.__init__.py:CmppTool.terminate_ismg()]socket连接不存在或已不在线，操作无效。')
        # 请求断开ISMG
        self._so.write(terminate_req.TerminateReq().message, event='terminate_ismg')
        # 断开socket连接
        self._so.close_socket()

    def submit_msg(self, message: str, phone_numbers: list):
        """
        发送信息
        """
        # 目的号码格式校验
        if not phone_numbers or type(phone_numbers) is not list:
            raise SMSServiceException(
                f'[tcp.cmpp.__init__.py:CmppTool.submit_msg()]'
                f'目的号码phone_numbers有误，其类型需为list，且每个元素均为正确格式的手机号码。phone_numbers:{phone_numbers}')
        else:
            for x in phone_numbers:
                if not x or type(x) is not str or str.strip(x) == '' or not re.search(REGEX['MOBILE_PHONE'], x):
                    raise SMSServiceException(f"[tcp.cmpp.__init__.py:CmppTool.submit_msg()]phone_numbers存在某元素有误, "
                                              f"有误的phoneNumber:{x}")
        # 消息内容校验
        if message is None or type(message) is not str or str.strip(message) == '':
            raise SMSServiceException(
                f'[tcp.cmpp.__init__.py:CmppTool.submit_msg()]'
                f'消息内容message有误，其需为String类型。message:{message}')
        # socket连接是否还在线
        if not self._so.is_online():
            raise SMSServiceException(f'[tcp.cmpp.__init__.py:CmppTool.submit_msg()]socket连接不存在或已不在线，操作无效。')
        # 是否需要做长短信拆分
        _split_send = False
        _split_count = NUMBERS['ONE']
        if len(message) > NUMBERS['SEVENTY']:
            # 需要拆分
            _split_send = True
            # 计算拆分后的条数
            _remainder = len(message) % NUMBERS['SIXTY_SEVEN']
            if _remainder != NUMBERS['ZERO']:
                _split_count += len(message) // NUMBERS['SIXTY_SEVEN']
            else:
                _split_count = len(message) // NUMBERS['SIXTY_SEVEN']
        # SP->ISMG发送消息的请求参数（需要状态报告，故只能对每个号码单发）
        for x in phone_numbers:
            if _split_send:
                # 拆分次数+1。每对一个号码做一次长短信拆分业务，均视为单独的一组。
                self._msg_split_key += NUMBERS['ONE']
                logger.info(
                    f"[CmppTool.submit_msg()][v{self._cmpp_version}]"
                    f"即将做第{self._msg_split_key}组长短信拆分业务，目标手机号:{x}。")
                # 对于长短信，逐条发送拆分过的短信
                current_record = {
                    'message': {},
                    # 拆分消息总条数
                    'total_count': _split_count,
                    # 已收到响应的拆分消息成功条数。如果某条失败，则整体失败
                    'res_success_count': NUMBERS['ZERO'],
                    # 已收到ISMG状态报告成功的拆分消息条数。如果某条失败，则整体失败。
                    'reported_success_count': NUMBERS['ZERO'],
                    # 存放所有状态报告
                    'all_report': [],
                    # 上一次收到状态报告的时间。用于清除异常留存的拆分记录数据，防止内存泄漏。注册时间当作首首次接收时间。
                    'last_report_timestamp': int(time.time()),
                    # 主短信的seq_id
                    'main_seq_id': None,
                    # 主短信的msg_id
                    'main_msg_id': None,
                    # True标志着该组数据已经无用，待自动删除了
                    'invalid': False,
                    # 被标记为无用时的时间戳（秒级）
                    'invalid_timestamp': None
                }
                for i in range(_split_count):
                    _current_count = i + NUMBERS['ONE']
                    _msg_id = _current_count
                    _mark = MESSAGE_SPLIT_MARK_PREFIX + struct.pack('!L', _msg_id) + \
                            struct.pack('!L', _split_count) + struct.pack('!L', _current_count)
                    _content = ''
                    if _current_count == _split_count:
                        _content = message[NUMBERS['SIXTY_SEVEN'] * i:]
                    else:
                        _content = message[NUMBERS['SIXTY_SEVEN'] * i: _current_count * NUMBERS['SIXTY_SEVEN']]
                    obj_msg = submit_req.SubmitReq(
                        version=self._cmpp_version, msg_src=self._sp_id, msg_content=message, dest_terminal_id=[x],
                        src_id=self._access_number)
                    # 给主短信seq_id赋值
                    if i == NUMBERS['ZERO']:
                        current_record['main_seq_id'] = obj_msg.sequence
                    # 给current_record添加一条message数据
                    current_record['message'][_current_count] = {
                        # 该条消息的序列号
                        'seq_id': obj_msg.sequence,
                        # 要发送的具体消息
                        'message': obj_msg.message,
                        # 该条消息是否已收到服务器响应
                        'received_res': False,
                        # 收到的响应是成功才算业务成功
                        'service_success': False
                    }
                # 向socket消息监听事件注册该组长短信拆分发送记录
                self._so.registry_split_rec(self._msg_split_key, current_record)
                # SP-ISMG发送消息
                for current_count, value in current_record['message'].items():
                    self._so.write(value['message'], event=f'[split:{current_count}]submit_msg->{x}')
            else:
                submit_params = submit_req.SubmitReq(
                    version=self._cmpp_version, msg_src=self._sp_id, msg_content=message, dest_terminal_id=[x],
                    src_id=self._access_number)
                # SP-ISMG发送消息
                self._so.write(submit_params.message, event=f'submit_msg->{x}')
