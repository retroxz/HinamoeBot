# -*- coding: utf-8 -*-
# @Time    : 2021/9/27 16:42
# @Author  : retroxz
# @Email   : zzxee666@gmail.com
# @File    : dynamic.py

__author__ = "retroxz"

from plugins.bilibili.api.base_request import request
from plugins.bilibili.utils.cache_bot import cache


class dynamic:
    @classmethod
    async def get_new_dynamic(cls):
        url = 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/dynamic_new'
        cookies = cache.get('bili_cookie')
        params = {
            'type_list': '268435455',
            'from': 'weball',
            'platform': 'web',
        }
        return await request('GET', url, params=params, cookies=cookies)

