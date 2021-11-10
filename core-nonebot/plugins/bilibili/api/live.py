#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author     :retroxz
@Date       :2021/11/10 23:00
@file       :live.py
@GitHub     :https://github.com/retroxz
"""


from .base_request import request
from ..utils.cache_bot import cache


async def get_live_status_by_uids(uids):
    url = 'https://api.live.bilibili.com/room/v1/Room/get_status_info_by_uids'
    # 读取cookies
    cookies = cache.get('bili_cookie')
    data = {
        'uids': uids,
        'csrf': cookies['bili_jct']
    }
    return await request('POST', url, json=data)
