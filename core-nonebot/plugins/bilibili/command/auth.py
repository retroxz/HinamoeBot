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
from plugins.bilibili.api.auth import get_login_url,get_login_info
from plugins.bilibili.utils.qr import *
from nonebot.adapters.cqhttp.message import MessageSegment, Message
from nonebot import require
from utils.logger import logger

scheduler = require("nonebot_plugin_apscheduler").scheduler


bili_auth = on_command('bili_auth', permission=SUPERUSER)


@bili_auth.handle()
async def _(bot: Bot, event: PrivateMessageEvent):
    # 获取扫码登录二维码
    login = await get_login_url()
    base64_str = generate_bili_auth_qr(login['url'])
    await bili_auth.send(MessageSegment.image(f"base64://{base64_str}"))
    logger.info('用户申请扫码登录哔哩哔哩')
    # 设置登陆验证定时任务
    scheduler.add_job(get_login_info, 'interval', seconds=20, id='login')
    return


async def verify_bili_login():
    logger.info('开始验证哔哩哔哩登录')
    response = await get_login_info()