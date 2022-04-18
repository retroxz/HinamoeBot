#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author     :retroxz
@Date       :2021/11/10 22:19
@file       :__init__.py.py
@GitHub     :https://github.com/retroxz
"""

from nonebot import require
from utils.logger import logger
from .dynamic import get_new_dynamic_task
from .live import get_live_status_task

scheduler = require("nonebot_plugin_apscheduler").scheduler


@scheduler.scheduled_job('interval', seconds=45)
async def task():
    """
    定时任务入口
    :return:
    """
    logger.info('直播检测任务')
    await get_live_status_task()
    logger.info('动态检测任务')
    await get_new_dynamic_task()

