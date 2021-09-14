# !/usr/bin/env python3
# coding=utf-8

from nonebot import on_message
from nonebot.adapters import Bot, Event
from nonebot.typing import T_State
from .lyric import words


lyric = on_message()

@lyric.handle()
async def _(bot: Bot, event: Event, state: T_State):
    for word in words:
        try:
            index = word.index(event.raw_message)
            if index < len(word)- 1:
                await lyric.finish(word[index + 1])
        except ValueError:
            pass