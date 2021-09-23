# -*- coding: utf-8 -*-
# @Time    : 2021/9/23 16:39
# @Author  : retroxz
# @Email   : zzxee666@gmail.com
# @File    : subscribe.py

__author__ = "retroxz"

from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent, PrivateMessageEvent

# 订阅

subscribe = on_command('新增订阅')


@subscribe.handle()
async def _(bot: Bot, event: PrivateMessageEvent):
    pass


@subscribe.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    await subscribe.send('群聊响应')