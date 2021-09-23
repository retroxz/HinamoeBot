#!/usr/bin/env python3
# coding=utf-8

"""
@File: __init__.py.py
@Author: retroxz
@Email: zzxee666@gmail.com
@Date: 2021/04/23
"""

from .plugin_data import Plugin_Data


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


async def get_card_name(bot, group_id, user_id):
    """
    获取用户群名片信息
    :param group_id:
    :param user_id:
    :return:
    """
    card_info = await bot.call_api('get_group_member_info', group_id, user_id)
    card = card_info['nickname'] if card_info['card'] == '' else card_info['card']
    return card


def is_admin(bot, event):
    """
    检测该用户是否为管理
    :param bot:
    :param event:
    :return:
    """
    if str(event.user_id) in bot.config.superusers:
        return True
    if event.message_type == 'private':
        return True
    if event.message_type == 'group' and event.sender.role == 'member':
        return False