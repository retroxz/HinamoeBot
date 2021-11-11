#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author     :retroxz
@Date       :2021/11/11 22:04
@file       :push_manager.py
@GitHub     :https://github.com/retroxz
"""

import time
import nonebot
import inspect
from nonebot.adapters.cqhttp import MessageSegment, Message


async def generate_live_start_message(sub, live):
    """
    构建直播开始推送消息
    :param sub:
    :param live:
    :return:
    """
    BILI_LIVE_URL_PREFIX = 'https://live.bilibili.com/'
    msg_template = F"""
        {live['uname']}的直播间开播啦！
        标题：{live['title']}
        开播时间：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(live['live_time']))}
        传送门：{BILI_LIVE_URL_PREFIX}{live['room_id']}
    """

    # 开启了艾特全体
    if sub['at_all'] == 1:
        # 检测bot是否有管理员
        bot = list(nonebot.get_bots().values())[0]
        bot_info = await bot.call_api('get_group_member_info', **{
            'group_id': sub['qid'],
            'user_id': bot.self_id
        })

        if bot_info['role'] in ['owner', 'admin']:
            # bot拥有管理员权限 可以艾特全体
            msg_template = F"{MessageSegment.at('all')}{msg_template}"

    return Message(inspect.cleandoc(msg_template))


async def generate_live_end_message(live, last_push_log):
    timestamp = int(time.time()) - last_push_log[0]['create_time']
    hour = int(timestamp / 3600)
    min = int((timestamp - (hour * 3600)) / 60)
    second = timestamp -  (hour * 3600) - (min * 60)
    msg_template = F"""
        {live['uname']}下播啦！
        本次直播时长："""
    msg_template += F"{hour}小时" if hour else ''
    msg_template += F"{min}分钟" if min else ''
    msg_template += F"{second}秒" if second else ''
    return Message(inspect.cleandoc(msg_template))
