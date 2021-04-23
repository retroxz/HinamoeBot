#!/usr/bin/env python3
#coding=utf-8  

"""
@File: logger.py
@Author: retroxz
@Email: zzxee666@gmail.com
@Date: 2021/04/23

logger 工具类
"""


import sys
from datetime import datetime
from rich import print

# 颜色设置
LOG_COLORS_CONFIG = {
    'DEBUG': 'cyan',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'red',
}

# 日志格式化设置
LOG_FORMATTER = '[bold {}]{} ({}) {}[/bold {}]'

def current_date(formatter = '%Y-%m-%d %H:%M:%S') -> str:
    """
    输出当前日期字符串
    :param formatter: 格式化字符串
    :return:
    """
    return datetime.now().strftime(formatter)


def console(level, message):
    """
    输出日志
    :param level: 日志等级
    :param message: 日志内容
    :return:
    """
    a = LOG_FORMATTER.format(
        LOG_COLORS_CONFIG[level.upper()],
        current_date(),
        level,
        message,
        LOG_COLORS_CONFIG[level.upper()]
    )
    print(a)


def debug(message):
    """
    输出DEBUG等级日志
    :param message:
    :return:
    """
    method_name = sys._getframe().f_code.co_name
    console(method_name, message)


def info(message):
    """
    输出INFO等级日志
    :param message:
    :return:
    """
    method_name = sys._getframe().f_code.co_name
    console(method_name, message)


def warning(message):
    """
    输出WARNING等级日志
    :param message:
    :return:
    """
    method_name = sys._getframe().f_code.co_name
    console(method_name, message)


def error(message):
    """
    输ERROR等级日志
    :param message:
    :return:
    """
    method_name = sys._getframe().f_code.co_name
    console(method_name, message)

def critical(message):
    """
    输CRITICAL等级日志
    :param message:
    :return:
    """
    method_name = sys._getframe().f_code.co_name
    console(method_name, message)