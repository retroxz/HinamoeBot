#!/usr/bin/env python3
# coding=utf-8

"""
@File: __init__.py.py
@Author: retroxz
@Email: zzxee666@gmail.com
@Date: 2021/04/23
"""

from .logger import debug, info, warning, error, critical
from .plugin_data import Plugin_Data


def is_integer(s):
    """
    validate param is integer
    :param s:
    :return:
    """
    try:
        int(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False
