"""
回调响应封装
"""
from smssdk.utils.values import CALLBACK_CODE


def callback_success(data: dict = None) -> dict:
    res = CALLBACK_CODE['SUCCESS']
    res['data'] = data
    return res


def callback_failed(data: dict = None) -> dict:
    res = CALLBACK_CODE['FAILED']
    res['data'] = data
    return res
