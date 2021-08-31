# !/usr/bin/env python3
# coding=utf-8

from nonebot import on_keyword
from nonebot.adapters import Bot, Event
from nonebot.typing import T_State
from datetime import datetime
from .greetings import Greeting
from utils import db

morning = on_keyword({'早','早安','早啊','早呀','早上好','早上花'})

@morning.handle()
async def _(bot: Bot, event: Event, state: T_State):
    current_hour = datetime.now().hour
    if current_hour < 6:
        await morning.finish(Greeting.morning_early.substitute())
    if current_hour >= 11:
        await morning.finish(Greeting.morning_late.substitute())

    # 查找打卡记录
    db.db_query()