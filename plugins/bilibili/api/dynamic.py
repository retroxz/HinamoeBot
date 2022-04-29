# -*- coding: utf-8 -*-
# @Time    : 2021/9/27 16:42
# @Author  : retroxz
# @Email   : zzxee666@gmail.com
# @File    : dynamic.py

__author__ = "retroxz"

from plugins.bilibili.api.base_request import request


async def get_new_dynamic(uid, offset_dynamic_id='0'):
    url = 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history'
    params = {
        'host_uid': uid,
        'offset_dynamic_id': offset_dynamic_id,
        'need_top': '0'
    }
    return await request('GET', url, params=params)

