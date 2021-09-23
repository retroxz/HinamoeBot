#!/usr/bin/env python3
# coding=utf-8

"""
@File: __init__.py.py
@Author: retroxz
@Email: zzxee666@gmail.com
@Date: 2021/04/23
"""

import re
import nonebot
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


async def get_card_name(group_id, user_id, bot=None, ):
    """
    获取用户群名片信息
    :param bot:
    :param group_id:
    :param user_id:
    :return:
    """

    if bot is None:
        bot = list(nonebot.get_bots().values())[0]

    card_info = await bot.call_api('get_group_member_info', group_id=group_id, user_id=user_id)
    card = card_info['nickname'] if card_info['card'] == '' else card_info['card']
    return card


def is_admin(event, bot=None):
    """
    检测该用户是否为管理
    :param bot:
    :param event:
    :return:
    """

    if bot is None:
        bot = list(nonebot.get_bots().values())[0]

    if str(event.user_id) in bot.config.superusers:
        return True
    if event.message_type == 'private':
        return True
    if event.message_type == 'group' and event.sender.role == 'member':
        return False


def get_event_id_and_type(event):
    # 获取事件类型和群号
    qtype = event.message_type
    qid = event.user_id if qtype == 'private' else event.group_id
    return qtype, qid


async def get_group_info(group_id, bot=None):
    """
    获取群信息
    :param bot:
    :param group_id:
    :return:
    """

    if bot is None:
        bot = list(nonebot.get_bots().values())[0]

    return await bot.call_api('get_group_info', group_id=group_id)


def filter_emoji(desstr, restr=''):
    """
    过滤表情
    """
    try:
        co = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return co.sub(restr, desstr)
