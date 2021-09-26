#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
@Author         : retroxz
@Date           : 2021/9/24 21:48
@Description    : None
@GitHub         : https://github.com/retroxz
"""

import asyncio
from .base_request import request

__author__ = "retroxz"

"""
    Bilibili 鉴权相关
"""


async def get_login_url():
    url = 'http://passport.bilibili.com/qrcode/getLoginUrl'
    response = await request('GET', url)
    return response.get('data')


if __name__ == '__main__':
    test_loop = asyncio.get_event_loop()
    test_loop.run_until_complete(get_login_url())