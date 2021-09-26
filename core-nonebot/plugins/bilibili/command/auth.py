#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
@Author         : retroxz
@Date           : 2021/9/24 22:04
@Description    : None
@GitHub         : https://github.com/retroxz
"""
__author__ = "retroxz"

from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, PrivateMessageEvent
from nonebot.permission import SUPERUSER
from plugins.bilibili.api.auth import get_login_url
from plugins.bilibili.utils.qr import *
from nonebot.adapters.cqhttp.message import MessageSegment, Message


bili_auth = on_command('bili_auth', permission=SUPERUSER)


@bili_auth.handle()
async def _(bot: Bot, event: PrivateMessageEvent):
    login = await get_login_url()
    base64_str = generate_bili_auth_qr(login['url'])
    await bili_auth.finish(MessageSegment.image(f"base64://{base64_str}"))

