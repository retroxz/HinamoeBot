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
import nonebot


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


async def get_card_name(group_id, user_id):
    bot = list(nonebot.get_bots().values())[0]
    # 获取群名片
    card_info = await bot.call_api('get_group_member_info', group_id, user_id)
    card = card_info['nickname'] if card_info['card'] == '' else card_info['card']
    return card

def is_admin(bot, event):
    if str(event.user_id) in bot.config.superusers:
        return True
    if event.message_type == 'private':
        return True
    if event.message_type == 'group' and event.sender.role == 'member':
        return False