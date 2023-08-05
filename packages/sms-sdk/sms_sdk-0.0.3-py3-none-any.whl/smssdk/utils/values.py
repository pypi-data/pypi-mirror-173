"""
一些常量
"""

""" 请求地址 """
URLS = {
    'TOKEN': '/api/v2/auth',
    'BATCH_SMS': '/api/v2/send',
    'P2P_SMS': '/api/v2/p2p'
}

""" 后台统一http响应相关信息 """
RESPONSE_INFO = {
    'CODE_OBJ': 'resultCode',
    'DATA': 'data',
    'RESPONSE_CODE': 'code',
    'RESPONSE_MESSAGE': 'message',
    'SUCCESS_CODE': 0,
    'AUTH_NAME': 'Authorization'
}

""" 后台api固定headers """
STABLE_HEADERS = {
    'CONTENT_TYPE': 'application/json;charset=utf-8'
}

""" 正则 """
REGEX = {
    'MOBILE_PHONE': '^1(3\\d|4[5-9]|5[0-35-9]|6[567]|7[0-8]|8\\d|9[0-35-9])\\d{8}$'
}

""" CMPP协议command_id """
CMPP_COMMAND_ID = {
    # SP->ISMG连接
    'CMPP_CONNECT': 0x00000001,
    # SP->ISMG断开连接
    'CMPP_TERMINATE': 0x00000002,
    # SP->ISMG发送信息
    'CMPP_SUBMIT': 0x00000004,
    # SP->ISMG连接应答
    'CMPP_CONNECT_RESP': 0x80000001,
    # SP->ISMG断开连接应答
    'CMPP_TERMINATE_RESP': 0x80000002,
    # SP->ISMG发送信息应答
    'CMPP_SUBMIT_RESP': 0x80000004,
    # ISMG->SP发送信息
    'CMPP_DELIVER': 0x00000005,
    # 激活测试
    'CMPP_ACTIVE_TEST': 0x00000008
}

""" SP->ISMG:CMPP_CONNECT_RESP status """
CMPP_CONNECT_RESP_STATUS = {
    # 成功
    'SUCCESS': {
        'code': 0,
        'meaning': '成功'
    },
    # 消息结构有误
    'MSG_FORMAT_ERROR': {
        'code': 1,
        'meaning': '消息结构有误'
    },
    # 非法源地址
    'INVALID_SOURCE_ADDR': {
        'code': 2,
        'meaning': '非法源地址'
    },
    # 认证错误
    'AUTH_FAILED': {
        'code': 3,
        'meaning': '认证错误'
    },
    # 版本太高
    'VERSION_TOO_HIGH': {
        'code': 4,
        'meaning': '版本太高'
    },
    # 其它错误
    'OTHER_ERROR': {
        'code': 5,
        'meaning': '其它错误'
    },
}

""" SP->ISMG:CMPP_SUBMIT_RESP v2.0 result """
CMPP_SUBMIT_RESP_RESULT_V2 = {
    # 正确
    'SUCCESS': {
        'result': 0,
        'meaning': '正确'
    },
    # 消息结构有误
    'MSG_FORMAT_ERROR': {
        'result': 1,
        'meaning': '消息结构有误'
    },
    # 命令字错
    'COMMAND_ERROR': {
        'result': 2,
        'meaning': '命令字错'
    },
    # 消息序号重复
    'MSG_NUMBER_DUPLICATE': {
        'result': 3,
        'meaning': '消息序号重复'
    },
    # 消息长度错误
    'MSG_LENGTH_PARAM_ERROR': {
        'result': 4,
        'meaning': '消息长度错误'
    },
    # 资费代码错误
    'FEE_CODE_ERROR': {
        'result': 5,
        'meaning': '资费错误'
    },
    # 超过最大信息长度限制
    'MSG_LENGTH_EXCEED': {
        'result': 6,
        'meaning': '超过最大信息长度限制'
    },
    # 业务代码错
    'SERVICE_PROGRAM_ERROR': {
        'result': 7,
        'meaning': '业务代码错'
    },
    # 流量控制错
    'FLOW_CONTROL_ERROR': {
        'result': 8,
        'meaning': '流量控制错'
    },
    # 其它错误
    'OTHER_ERROR': {
        'result': 9,
        'meaning': '其它错误'
    },
}

""" SP->ISMG:CMPP_SUBMIT_RESP v3.0 result """
CMPP_SUBMIT_RESP_RESULT_V3 = {
    # 正确
    'SUCCESS': {
        'result': 0,
        'meaning': '正确'
    },
    # 消息结构有误
    'MSG_FORMAT_ERROR': {
        'result': 1,
        'meaning': '消息结构有误'
    },
    # 命令字错
    'COMMAND_ERROR': {
        'result': 2,
        'meaning': '命令字错'
    },
    # 消息序号重复
    'MSG_NUMBER_DUPLICATE': {
        'result': 3,
        'meaning': '消息序号重复'
    },
    # 消息长度错误
    'MSG_LENGTH_PARAM_ERROR': {
        'result': 4,
        'meaning': '消息长度错误'
    },
    # 资费代码错误
    'FEE_CODE_ERROR': {
        'result': 5,
        'meaning': '资费错误'
    },
    # 超过最大信息长度限制
    'MSG_LENGTH_EXCEED': {
        'result': 6,
        'meaning': '超过最大信息长度限制'
    },
    # 业务代码错
    'SERVICE_PROGRAM_ERROR': {
        'result': 7,
        'meaning': '业务代码错'
    },
    # 流量控制错
    'FLOW_CONTROL_ERROR': {
        'result': 8,
        'meaning': '流量控制错'
    },
    # 本网关不负责服务此计费号码
    'OTHER_ERROR': {
        'result': 9,
        'meaning': '本网关不负责服务此计费号码'
    },
    # 本网关不负责服务此计费号码
    'SRC_ID_ERROR': {
        'result': 10,
        'meaning': 'Src_Id错误'
    },
    # Msg_src错误
    'MSG_SRC_ERROR': {
        'result': 11,
        'meaning': 'Msg_src错误'
    },
    # Fee_terminal_Id错误
    'FEE_TERMINAL_ID_ERROR': {
        'result': 12,
        'meaning': 'Fee_terminal_Id错误'
    },
    # Dest_terminal_Id错误
    'DEST_TERMINAL_ID': {
        'result': 13,
        'meaning': 'Dest_terminal_Id错误'
    }
}

""" 常用数字 """
NUMBERS = {
    'ZERO': 0,
    'ONE': 1,
    'MAX_PORT': 65535,
    'THREE_HUNDREDS': 300,
    'SEVENTY': 70,
    'SIXTY_SEVEN': 67
}

""" cmpp2.0/3.0协议中ISMG->SP消息是否为状态报告 """
CMPP_REGISTERED_DELIVERY = {
    'NOT_REPORT': 0,
    'IS_REPORT': 1
}

""" 回调响应码 """
CALLBACK_CODE = {
    'SUCCESS': {
        'code': 0,
        'message': '成功'
    },
    'FAILED': {
        'code': 1,
        'message': '异常'
    },
}

""" 支持的CMPP协议版本号 """
CMPP_VERSION = {
    'TWO': 2,
    'THREE': 3,
}

""" 长短信拆分标志前缀 """
MESSAGE_SPLIT_MARK_PREFIX = b'/x05/x00/x03'

""" ISMG->SP:CMPP_DELIVER事件中，状态报告里的stat """
REPORT_STAT = {
    'DELIVRD': {
        'MESSAGE_STATE': 'DELIVERED',
        'FINAL_MESSAGE_STATE': 'DELIVRD',
        'DESCRIPTION': 'Message is delivered to destination.'
    },
    'EXPIRED': {
        'MESSAGE_STATE': 'EXPIRED',
        'FINAL_MESSAGE_STATE': 'EXPIRED',
        'DESCRIPTION': 'Message validity period has expired.'
    },
    'DELETED': {
        'MESSAGE_STATE': 'DELETED',
        'FINAL_MESSAGE_STATE': 'DELETED',
        'DESCRIPTION': 'Message has been deleted.'
    },
    'UNDELIV': {
        'MESSAGE_STATE': 'UNDELIVERABLE',
        'FINAL_MESSAGE_STATE': 'UNDELIV',
        'DESCRIPTION': 'Message is undeliverable.'
    },
    'ACCEPTD': {
        'MESSAGE_STATE': 'ACCEPTED',
        'FINAL_MESSAGE_STATE': 'ACCEPTD',
        'DESCRIPTION': 'Message is in accepted state(i.e. has been manually read on behalf of the subscriber by '
                       'customer service). '
    },
    'UNKNOWN': {
        'MESSAGE_STATE': 'UNKNOWN',
        'FINAL_MESSAGE_STATE': 'UNKNOWN',
        'DESCRIPTION': 'Message is in invalid state.'
    },
    'REJECTD': {
        'MESSAGE_STATE': 'REJECTED',
        'FINAL_MESSAGE_STATE': 'REJECTD',
        'DESCRIPTION': 'Message is in a rejected state.'
    }
}

""" 长短信拆分时，接收状态报告最大等待时长。单位s """
MAX_REPORT_WAIT_TIME = 60
