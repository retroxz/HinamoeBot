# !/usr/bin/env python3
# coding=utf-8
from ..exception import BiliUserNotFoundException
from ..api.Space import Space as SpaceApi


async def get_user_info(uid):
    """
    获取bilibili用户资料卡
    :param uid: 用户uid或者昵称
    :return: 用户资料卡json
    """
    space = SpaceApi()
    if not uid.isdigit():
        search_info = await space.search_user(uid)
        if search_info['numResults'] == 0:
            raise BiliUserNotFoundException(uid)
        uid = search_info.get('result')[0]['mid']
    # 获取带粉丝数的用户信息
    user_card_info = await space.get_user_card_info(uid)
    # 获取带直播间的用户信息
    user_info = await space.get_user_info(uid)
    if not user_card_info:
        raise BiliUserNotFoundException(uid)
    user_card_info['card']['roomid'] = user_info['live_room']['roomid']
    return user_card_info['card']
