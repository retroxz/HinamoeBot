# !/usr/bin/env python3
# coding=utf-8
"""
    Error info template
"""

BILI_REQUEST_TIME_OUT = 'Bili request time out: {url}'

BILI_READ_TIME_OUT = 'Bili response read time out: {url}'

BILI_UNKNOWN_ERROR = """
Bili unknown error: {url}
{response.text}
"""
