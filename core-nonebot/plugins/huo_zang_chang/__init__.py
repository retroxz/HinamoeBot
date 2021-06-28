# !/usr/bin/env python3
# coding=utf-8

from nonebot import on_message
from nonebot.adapters import Bot, Event
from nonebot.typing import T_State
from .lyric import hzc


lyric = on_message()

@lyric.handle()
async def _(bot: Bot, event: Event, state: T_State):
    try:
        index = hzc.index(event.raw_message)
        if index < len(hzc)- 1:
            await lyric.finish(hzc[index + 1])
    except ValueError:
        pass