#!/usr/bin/env python
# -*-coding:utf-8 -*-

from .command import *
from utils.logger import logger
from utils import send_private_message
from plugins.bilibili.model.auth import auth_model
from plugins.bilibili.utils.cache_bot import cache
import asyncio
import nonebot
from nonebot import get_driver

driver = get_driver()


@driver.on_bot_connect
async def load_cookie(bot):
    # 从数据库加载cookie
    cookies = await auth_model.query_cache()
    if cookies:
        # 保存到缓存
        cache.set('bili_cookie', cookies)
        logger.success('哔哩哔哩Cookie加载成功')
    else:
        await send_private_message('哔哩哔哩Cookie不存在, 请使用/bili_auth 进行登录', list(bot.config.superusers)[0])
        logger.error('哔哩哔哩Cookie不存在, 请使用/bili_auth 进行登录')
