#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
@Author         : retroxz
@Date           : 2021/9/14 22:46
@Description    : None
@GitHub         : https://github.com/retroxz
"""

from .base_request import request

__author__ = "retroxz"

"""
    bilibili 搜索相关
"""


async def search_user_uid(uid):
    """
    搜索指定用户uid
    :param uid:
    :return:
    """
    # TODO: 优化代码结构 解决circular import
    from .. import BiliUserNotFoundException

    if uid.isdigit():
        return uid
    url = F"http://api.bilibili.com/x/web-interface/search/type?keyword={uid}&search_type=bili_user"
    response = await request('GET', url)
    if response['numResults'] == 0:
        raise BiliUserNotFoundException(uid)
    return response.get('result')[0]['mid'], response.get('result')[0]['room_id']
