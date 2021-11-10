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
from plugins.bilibili.api.auth import get_login_url, get_login_info
from plugins.bilibili.utils.qr import *
from nonebot.adapters.cqhttp.message import MessageSegment, Message
from nonebot import require
from utils.logger import logger
import datetime
from plugins.bilibili.utils.cache_bot import cache
from utils import send_private_message
from plugins.bilibili.model.auth import auth_model

scheduler = require("nonebot_plugin_apscheduler").scheduler


bili_auth = on_command('bili_auth', permission=SUPERUSER)


@bili_auth.handle()
async def _(bot: Bot, event: PrivateMessageEvent):
    # 储存申请二维码的qq
    cache.set('auth_qq', event.user_id)
    # 获取扫码登录二维码
    login = await get_login_url()
    base64_str = generate_bili_auth_qr(login['url'])
    await bili_auth.send(MessageSegment.image(f"base64://{base64_str}"))
    logger.info('用户申请扫码登录哔哩哔哩')
    # 设置登陆验证定时任务
    scheduler.add_job(verify_bili_login, 'interval', seconds=30, id='login')
    # 设置登陆验证超时
    scheduler.add_job(bili_qr_time, run_date=datetime.datetime.now()+datetime.timedelta(seconds=180),
                      id='verify_timeout')


async def verify_bili_login():
    response = await get_login_info()
    body = response.json()
    if body.get('code') == 0:
        scheduler.remove_job('login')
        cookies = {}
        for cookie in response.cookies.jar:
            cookies[cookie.name] = cookie.value

        # 保存到缓存
        cache.set('bili_cookie', cookies)
        # 持久化到数据库
        await auth_model.update_cache(cookies)
        scheduler.remove_job('verify_timeout')
        await send_private_message('哔哩哔哩账号登录成功', qid=cache.get('auth_qq'))


async def bili_qr_time():
    scheduler.remove_job('login')
    await send_private_message('二维码已失效 登录失败', qid=cache.get('auth_qq'))

