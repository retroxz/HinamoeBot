#!/usr/bin/env python
# -*-coding:utf-8 -*-

"""
@Author         : retroxz
@Date           : 2022/4/29 15:13
@Description    : None
@GitHub         : https://github.com/retroxz
"""

"""
    复读插件
"""

from nonebot import on_message
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent
from cacheout import Cache
from utils.config import Config

repeat = on_message(priority=10)

# 初始化缓存
cache = Cache()
cache.set('message_list', {})

# 读取配置
repeat_max = Config.get('repeat.max', 3)


@repeat.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    message_list = cache.get('message_list')
    if message_list.get(event.group_id) is None:
        message_list[event.group_id] = {
            'before': event.raw_message,
            'count': 1
        }
        cache.set('message_list', message_list)
        return

    if message_list[event.group_id]['before'] == event.raw_message:
        message_list[event.group_id]['count'] = message_list[event.group_id]['count'] + 1
        if message_list[event.group_id]['count'] == repeat_max:
            cache.set('message_list', message_list)
            await repeat.finish(event.message)
    else:
        message_list[event.group_id]['before'] = event.raw_message
        message_list[event.group_id]['count'] = 1
        cache.set('message_list', message_list)
        return
