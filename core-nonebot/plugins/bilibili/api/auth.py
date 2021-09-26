#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
@Author         : retroxz
@Date           : 2021/9/24 21:48
@Description    : None
@GitHub         : https://github.com/retroxz
"""

import asyncio
import httpx
from .base_request import request
from plugins.bilibili.utils.cache_bot import cache

__author__ = "retroxz"

"""
    Bilibili 鉴权相关
"""


async def get_login_url():
    url = 'http://passport.bilibili.com/qrcode/getLoginUrl'
    response = await request('GET', url)
    # 将oathKey缓存
    cache.set('bili_oauth_key', response['oauthKey'])
    return response


async def get_login_info():
    url = 'http://passport.bilibili.com/qrcode/getLoginInfo'
    oauth_key = cache.get('bili_oauth_key')
    params = {'oauthKey': oauth_key}
    response = await request('POST', url, data=params, origin=True)
    return response
