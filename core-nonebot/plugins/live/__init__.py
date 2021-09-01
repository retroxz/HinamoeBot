# !/usr/bin/env python3
# coding=utf-8  
__author__ = 'retroxz'

from nonebot.adapters.cqhttp.event import GroupBanNoticeEvent, GroupMessageEvent
from nonebot import on_command
from nonebot.adapters import Bot, Event
from nonebot.permission import SUPERUSER
import httpx
from utils.plugin_data import Plugin_Data

PLUGIN_NAME = 'live'
pd = Plugin_Data(PLUGIN_NAME)


band_room = on_command('绑定直播间', permission=SUPERUSER)

async def get_live_info(room_id):
    res = httpx.get('https://api.live.bilibili.com/xlive/web-room/v1/index/getInfoByRoom',
              params={'room_id': room_id}).json()
    if res['code'] != 0:
        await band_room.finish(F"找不到直播间{room_id}")


@band_room.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    if not isinstance(event, GroupMessageEvent):
        return
    room_id = event.get_message()
    live_info = await get_live_info(room_id)
    print(live_info)