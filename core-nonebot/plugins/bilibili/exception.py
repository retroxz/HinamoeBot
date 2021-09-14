# !/usr/bin/env python3
# coding=utf-8
from utils import is_integer


class PluginsBaseException(Exception):
    pass


class ParamsErrorException(PluginsBaseException):
    def __init__(self, param_name: str):
        self.param_name = param_name

    def __str__(self):
        return F"{self.param_name}参数格式错误"


class BiliUserNotFoundException(PluginsBaseException):
    def __init__(self, uid: str):
        self.uid = uid

    def __str__(self):
        return F"找不到{'uid' if is_integer(self.uid) else '昵称'}为{self.uid}的用户"


class BiliRequestError(PluginsBaseException):
    def __init__(self, url, msg):
        self.url = url
        self.msg = msg

    def __str__(self):
        error_msg = F"Bili API Request Error({self.url}): {self.msg}"
        return error_msg
