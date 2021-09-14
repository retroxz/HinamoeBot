# !/usr/bin/env python3
# coding=utf-8

"""
Space Service Class
"""
from typing import Optional

from .BaseRequest import request
from ..exception import BiliUserNotFoundException


async def get_user_space_info(uid):
    """
    获取bilibili用户空间详细信息
    :param uid: 用户uid或者昵称
    :return: 用户资料卡json
    """

    response = await request('GET', F"http://api.bilibili.com/x/space/acc/info?mid={uid}")
    if not response.get('data'):
        raise BiliUserNotFoundException(uid)
    return response.get('data')


async def get_user_card_info(uid):
    url = F"http://api.bilibili.com/x/web-interface/card?mid={uid}"
    response = await request('GET', url)
    if not response.get('data'):
        raise BiliUserNotFoundException(uid)
    return response.get('data')