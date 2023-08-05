"""
socket封装，cmpp专用
"""
import socket
import struct
import time

from zpystream import Stream

from smssdk.tcp import callback_success, callback_failed
from smssdk.tcp.cmpp.callback import BasicCallback
from smssdk.tcp.cmpp.resdata.router import parse_response
from smssdk.utils.exceptions import SMSServiceException
from smssdk.utils.logger import Logger
from smssdk.utils.values import CMPP_COMMAND_ID, CMPP_CONNECT_RESP_STATUS, CMPP_SUBMIT_RESP_RESULT_V2, \
    CMPP_SUBMIT_RESP_RESULT_V3, CMPP_VERSION, NUMBERS, REPORT_STAT, MAX_REPORT_WAIT_TIME

logger = Logger('tcp.cmpp.sockettool.__init__.py')


class Socket:
    def __init__(self, cmpp_version: int, host: str, port: int, callback: BasicCallback):
        """
        初始化socket参数
        :param cmpp_version: CMPP版本。2/3
        :param host: 地址
        :param port: 端口
        :param callback: 回调实现
        """
        self._version = cmpp_version
        self._host = host
        self._port = port
        self._callback = callback
        self._so = None
        # 记录长短信发送数据
        self._split_send_rec = {}
        # 所有长短新拆分消息的发送序列号和对应响应的msg_id。结构：{seq_id: res_msg_id, ...}
        self._split_seq_and_res_msg_id = {}
        # 暂存需要从_split_send_rec中删除的元素的key
        self._need_del_key = []
        # 暂存需要从_split_seq_and_res_msg_id中删除的元素的key
        self._need_del_msg_id_key = []

    def connect_socket(self):
        """
        连接socket服务
        """
        try:
            self._so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._so.connect((self._host, self._port))
            logger.info(f'[Socket.connect_socket()][v{self._version}][connect]socket连接成功。')
        except Exception as e:
            logger.exception(e,
                             f'[Socket._connect_socket()][v{self._version}]socket服务连接失败，'
                             f'host:{self._host}，port:{self._port}。')
            raise SMSServiceException(
                f'[tcp.cmpp.sockettool.__init__.py:Socket._connect_socket()][v{self._version}]socket服务连接失败，'
                f'host:{self._host}，port:{self._port}。')

    def close_socket(self):
        """
        断开socket服务
        """
        try:
            self._so.close()
            logger.info(f'[Socket.close_socket()][v{self._version}][close]socket已断开连接。')
        except Exception as e:
            logger.exception(e, '[Socket._close_socket()][v{self._version}]断开socket连接失败。')
            raise SMSServiceException(
                '[tcp.cmpp.sockettool.__init__.py:Socket._close_socket()][v{self._version}]断开socket连接失败。')

    def write(self, message, event):
        """
        socket客户端发送消息
        """
        try:
            self._so.send(message)
            logger.info(f'[Socket.write()][{event}][v{self._version}][send]{message.hex()}。')
        except Exception as e:
            logger.exception(e,
                             f'[Socket.write()][{event}][v{self._version}][send]socket send message failed，message:{message.hex()}')
            raise SMSServiceException(
                f'[tcp.cmpp.sockettool.__init__.py:Socket.write()][{event}][v{self._version}][send]'
                f'socket send message failed，message:{message.hex()}')

    def read(self):
        """
        持续监听服务端的消息
        """
        while 1:
            if getattr(self._so, '_closed'):
                logger.info(f'[Socket.read()]socket连接已关闭，读取服务端消息线程即将结束。')
                return
            response = None
            try:
                content_length = self._so.recv(4)
                if content_length:
                    length, = struct.unpack('!L', content_length)
                    response = content_length + self._so.recv(length - 4)
                    logger.info(f'[Socket.read()][recv]'
                                f'length:{length}，content:{response.hex()}。')
            except ConnectionAbortedError:
                logger.info(f'[Socket.read()]socket连接已关闭/断开，读取服务端消息线程即将结束。')
                return
            # 不同事件做不同处理
            parsed_res = parse_response(response, self._version)
            # 登录/连接ISMG响应
            if parsed_res.command_id == CMPP_COMMAND_ID['CMPP_CONNECT_RESP']:
                if parsed_res.status == CMPP_CONNECT_RESP_STATUS['SUCCESS']['code']:
                    self._callback.for_connect(callback_success())
                else:
                    ismg_res_status = parsed_res.status
                    failed_item = Stream(CMPP_CONNECT_RESP_STATUS.keys()).filter(
                        lambda x: CMPP_CONNECT_RESP_STATUS[x]['code'] == ismg_res_status).to_list()
                    if failed_item and len(failed_item) > 0:
                        self._callback.for_connect(callback_failed(CMPP_CONNECT_RESP_STATUS[failed_item[0]]))
                    else:
                        logger.warning(f'[Socket.read()][v{self._version}][CMPP_CONNECT_RESP]事件status异常，不在任何枚举值之中。')
                        self._callback.for_connect(callback_failed({}))
                    logger.info(f'[Socket.read()][v{self._version}][CMPP_CONNECT_RESP]事件异常，即将断开socket连接。')
                    self.close_socket()
            # 向ISMG提交消息事件响应
            elif parsed_res.command_id == CMPP_COMMAND_ID['CMPP_SUBMIT_RESP']:
                res_code = None
                if self._version == CMPP_VERSION['TWO']:
                    res_code = CMPP_SUBMIT_RESP_RESULT_V2
                else:
                    res_code = CMPP_SUBMIT_RESP_RESULT_V3
                # 是响应的长短信拆分的消息，找出长短信发送记录，做相关处理
                if len(self._split_seq_and_res_msg_id) > NUMBERS['ZERO'] and \
                        parsed_res.sequence in self._split_seq_and_res_msg_id.keys():
                    for k1, v1 in self._split_send_rec.items():
                        for k2, v2 in v1['message'].items():
                            if v2['seq_id'] == parsed_res.sequence:
                                self._split_seq_and_res_msg_id[v2['seq_id']] = parsed_res.msg_id
                                # 跳过已无效的记录
                                if v1['invalid']:
                                    logger.info(f'[Socket.read()][v{self._version}][CMPP_SUBMIT_RESP]'
                                                f'已跳过一条响应，因该条响应所在的拆分短信组已被置为无效，'
                                                f'seq:{parsed_res.sequence}，msg_id:{parsed_res.msg_id}。')
                                    break
                                # 提取该组seq_id
                                all_seq_ids = []
                                for k3, v3 in v1['message'].items():
                                    all_seq_ids.append(v3['seq_id'])
                                # 该条短信已收到响应
                                v1['message'][k2]['received_res'] = True
                                if v2['seq_id'] == v1['main_seq_id']:
                                    v1['main_msg_id'] = parsed_res.msg_id
                                # 该条成功，做记录
                                if parsed_res.result == res_code['SUCCESS']['result']:
                                    v1['res_success_count'] += NUMBERS['ONE']
                                    v1['message'][k2]['service_success'] = True
                                    # 该组拆分短信的所有响应接收完毕，做成功回调
                                    if v1['total_count'] == v1['res_success_count']:
                                        logger.info(
                                            f"[Socket.read()][v{self._version}][CMPP_SUBMIT_RESP][split]"
                                            f"第{k1}组长短信拆分业务响应正常，该组对应的拆分短信sequence分别为：{all_seq_ids}，"
                                            f"主msg_id为{v1['main_msg_id']}。即将发出成功回调。")
                                        self._callback.for_submit(callback_success({'msg_id': v1['main_msg_id']}))
                                # 该条异常，则所有失败，做失败回调，并删除该组记录
                                else:
                                    logger.info(
                                        f"[Socket.read()][v{self._version}][CMPP_SUBMIT_RESP][split]"
                                        f"第{k1}组长短信拆分业务失败，收到状态异常的响应，该组对应的拆分短信sequence分别为：{all_seq_ids}，"
                                        f"主msg_id为{v1['main_msg_id']}。即将发出失败回调。")
                                    ismg_res_result = parsed_res.result
                                    failed_item = Stream(res_code.keys()).filter(
                                        lambda x: res_code[x]['result'] == ismg_res_result).to_list()
                                    if failed_item and len(failed_item) > 0:
                                        self._callback.for_submit(callback_failed(
                                            {
                                                'msg_id': v1['main_msg_id'],
                                                'failed_res': res_code[failed_item[0]]
                                            }
                                        ))
                                    else:
                                        logger.warning(
                                            f'[Socket.read()][v{self._version}][CMPP_SUBMIT_RESP]['
                                            f'split]事件result异常，不在任何枚举值之中。')
                                        self._callback.for_submit(callback_failed({'msg_id': v1['main_msg_id']}))
                                    # 发生异常响应，该组记录置为过去式
                                    v1['invalid'] = True
                                    v1['invalid_timestamp'] = int(time.time())
                                    break
                    # 删除已invalid超过10分钟的拆分记录
                    self._del_invalid_records()
                # 普通短信发送响应
                else:
                    # 成功
                    if parsed_res.result == res_code['SUCCESS']['result']:
                        self._callback.for_submit(callback_success({'msg_id': parsed_res.msg_id}))
                    # 异常
                    else:
                        ismg_res_result = parsed_res.result
                        failed_item = Stream(res_code.keys()).filter(
                            lambda x: res_code[x]['result'] == ismg_res_result).to_list()
                        if failed_item and len(failed_item) > 0:
                            self._callback.for_submit(callback_failed(
                                {
                                    'msg_id': parsed_res.msg_id,
                                    'failed_res': res_code[failed_item[0]]
                                }
                            ))
                        else:
                            logger.warning(f'[Socket.read()][v{self._version}][CMPP_SUBMIT_RESP]事件result异常，不在任何枚举值之中。'
                                           f'msg_id:{parsed_res.msg_id}。')
                            self._callback.for_submit(callback_failed({'msg_id': parsed_res.msg_id}))
            # 向ISMG提交信息后，ISMG主动发送的状态报告
            elif parsed_res.command_id == CMPP_COMMAND_ID['CMPP_DELIVER']:
                if parsed_res.is_report:
                    # 是否是拆分短信对应的状态报告（规则：submit res msg id = report send msg id），如果是，做相关记录赋值及整合判断。
                    if len(self._split_seq_and_res_msg_id) > NUMBERS['ZERO'] and \
                            parsed_res.msg_id in self._split_seq_and_res_msg_id.values():
                        send_seq_id = None
                        for k0, v0 in self._split_seq_and_res_msg_id.items():
                            if v0 == parsed_res.msg_id:
                                send_seq_id = k0
                        for k1, v1 in self._split_send_rec.items():
                            for k2, v2 in v1['message'].items():
                                if v2['seq_id'] == send_seq_id:
                                    # 跳过已无效的记录
                                    if v1['invalid']:
                                        logger.info(f'[Socket.read()][v{self._version}][CMPP_DELIVER]'
                                                    f'已跳过一条状态报告，因该报告对应所在的拆分短信组已被置为无效，'
                                                    f'seq:{parsed_res.sequence}，msg_id:{parsed_res.msg_id}。')
                                        continue
                                    # 提取所有该组所有seq_id
                                    all_seq_ids = []
                                    for k3, v3 in v1['message'].items():
                                        all_seq_ids.append(v3['seq_id'])
                                    # 更新该组记录最近接收状态报告的时间
                                    v1['last_report_timestamp'] = int(time.time())
                                    # 该条状态报告成功（stat为DELIVRD）
                                    if parsed_res.callback_res['stat'] == REPORT_STAT['DELIVRD']['FINAL_MESSAGE_STATE']:
                                        v1['reported_success_count'] += NUMBERS['ONE']
                                        v1['all_report'].append(parsed_res.callback_res)
                                        # 如果收到stat为DELIVRD的报告数量达到总拆分条数，说明全部成功，即整个长短信业务成功
                                        if v1['reported_success_count'] == v1['total_count']:
                                            logger.info(
                                                f"[Socket.read()][v{self._version}][CMPP_DELIVER][split]"
                                                f"第{k1}组长短信拆分业务状态报告正常，该组对应的拆分短信sequence分别为：{all_seq_ids}，"
                                                f"主msg_id为{v1['main_msg_id']}。即将发出成功回调。")
                                            self._callback.for_submit_report(callback_success(
                                                {
                                                    'msg_id': v1['main_msg_id'],
                                                    'all_report': v1['all_report']
                                                }
                                            ))
                                            # 该组拆分消息的状态报告接收完毕，设为过去式
                                            v1['invalid'] = True
                                            v1['invalid_timestamp'] = int(time.time())
                                    # 该条状态报告异常（stat为DELIVRD）
                                    else:
                                        logger.info(
                                            f"[Socket.read()][v{self._version}][CMPP_DELIVER][split]"
                                            f"第{k1}组长短信拆分业务状态报告异常，收到状态stat非DELIVRD的状态报告，"
                                            f"该组对应的拆分短信sequence分别为：{all_seq_ids}，"
                                            f"msg_id:{v1['main_msg_id']}。即将发出失败回调。")
                                        v1['all_report'].append(parsed_res.callback_res)
                                        self._callback.for_submit_report(callback_failed(
                                            {
                                                'msg_id': v1['main_msg_id'],
                                                'all_report': v1['all_report']
                                            }
                                        ))
                                        # 该组消息拆分记录存在异常状态报告，整组记录设为过去式
                                        v1['invalid'] = True
                                        v1['invalid_timestamp'] = int(time.time())
                                    break
                        # 检查删除已invalid5分钟的记录
                        self._del_invalid_records()
                        # 顺带检查是否有异常记录，有的话删了
                        now_timestamp = int(time.time())
                        need_del_key_by_time = []
                        for k, v in self._split_send_rec.items():
                            if now_timestamp - v['last_report_timestamp'] > MAX_REPORT_WAIT_TIME:
                                need_del_key_by_time.append(k)
                        if need_del_key_by_time:
                            self._del_invalid_records(need_del_key_by_time)
                    # 普通短信的状态报告
                    else:
                        if parsed_res.callback_res['stat'] == REPORT_STAT['DELIVRD']['FINAL_MESSAGE_STATE']:
                            self._callback.for_submit_report(callback_success(
                                {
                                    'msg_id': parsed_res.msg_id,
                                    'all_report': [parsed_res.callback_res]
                                }
                            ))
                        else:
                            logger.info(
                                f"[Socket.read()][v{self._version}][CMPP_DELIVER][split]"
                                f"普通短信状态报告异常，收到状态stat非DELIVRD的状态报告，"
                                f"msg_id:{parsed_res.msg_id}。即将发出失败回调。")
                            self._callback.for_submit_report(callback_failed(
                                {
                                    'msg_id': parsed_res.msg_id,
                                    'all_report': [parsed_res.callback_res]
                                }
                            ))

            # 激活测试/心跳
            elif parsed_res.command_id == CMPP_COMMAND_ID['CMPP_ACTIVE_TEST']:
                # logger.info(f'[Socket.read()][v{self._version}]收到激活测试。')
                pass

    def is_online(self):
        """
        socket连接是还处于连接状态
        :return: True是，False否
        """
        return self._so and not getattr(self._so, '_closed')

    def registry_split_rec(self, k: int, v: dict):
        """
        注册新的长短新拆分发送记录、并提取消息序列号
        :param k: 该组记录的key
        :param v: 该组记录的数据
        """
        self._split_send_rec[k] = v
        for k1, v1 in v['message'].items():
            self._split_seq_and_res_msg_id[v1['seq_id']] = None

    def _del_key_from_registry_split_rec(self, k: list):
        """
        从拆分消息记录中删除若干组数据
        :param k: keys
        """
        if not k:
            return
        for x in k:
            del self._split_send_rec[x]

    def _del_key_from_seq_and_res_msg_id(self, k: list):
        """
        从seq_id:msg_id记录中删除若干组数据
        :param k: keys
        """
        if not k:
            return
        for x in k:
            del self._split_seq_and_res_msg_id[x]

    def _del_invalid_records(self, a_k: list = None):
        """
        传递k时，从拆分记录中删除key为k的记录及可能存在的关联seq_id:msg_id记录；
        不传递k时，检索全部拆分数据记录，从中删除invalid已超过5分钟的元素以及其关联的seq_id:msg_id记录
        :return:
        """
        if not a_k:
            all_record_key = []
            all_seq_ids_del = []
            for k, v in self._split_send_rec.items():
                if v['invalid'] and int(time.time()) - v['invalid_timestamp'] > NUMBERS['THREE_HUNDREDS']:
                    all_record_key.append(k)
                    for k1, v1 in v['message'].items():
                        if v1['seq_id'] in self._split_seq_and_res_msg_id:
                            all_seq_ids_del.append(v1['seq_id'])
            if all_seq_ids_del:
                self._del_key_from_seq_and_res_msg_id(all_seq_ids_del)
            if all_record_key:
                self._del_key_from_registry_split_rec(a_k)
        else:
            for x in a_k:
                v = self._split_send_rec[x]
                all_seq_ids_del = []
                for k1, v1 in v['message'].items():
                    if v1['seq_id'] in self._split_seq_and_res_msg_id:
                        all_seq_ids_del.append(v1['seq_id'])
                if all_seq_ids_del:
                    self._del_key_from_seq_and_res_msg_id(all_seq_ids_del)
            self._del_key_from_registry_split_rec(a_k)
