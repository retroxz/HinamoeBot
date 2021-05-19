# !/usr/bin/env python3
# coding=utf-8
import nonebot
from nonebot import on_startswith
from dateutil.parser import parse
from nonebot.adapters import Bot, Event
from .model import *
from utils import Plugin_Data
from .config import *


PLUGIN_NAME = 'danmaku'
DEFAULT_ROOM_ID = nonebot.get_driver().config.danmaku_default_room_id
pd = Plugin_Data(PLUGIN_NAME)


danmaku_rank = on_startswith('#弹幕排行')


@danmaku_rank.handle()
async def _(bot: Bot, event:Event):
    current_date = {}
    try:
        current_date = parse(event.raw_message.split('#弹幕排行')[-1])
    except:
        await danmaku_rank.finish(F"日期格式不正确呀\n例如:05-02")
    # 查询此人绑定的直播间
    pd.query(Config(id=event))
    # result = await danmaku_rank(current_date,)