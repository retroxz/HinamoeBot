# !/usr/bin/env python3
# coding=utf-8
import nonebot
from nonebot import on_startswith
from dateutil.parser import parse
from nonebot.adapters import Bot, Event
from .model import *
from utils import Plugin_Data
from .config import *
import httpx


PLUGIN_NAME = 'danmaku'
DEFAULT_ROOM_ID = nonebot.get_driver().config.danmaku_default_room_id
pd = Plugin_Data(PLUGIN_NAME)


# danmaku_rank = on_startswith('#弹幕排行')
#
#
# @danmaku_rank.handle()
# async def _(bot: Bot, event:Event):
#     current_date = {}
#     try:
#         current_date = parse(event.raw_message.split('#弹幕排行')[-1])
#     except:
#         await danmaku_rank.finish(F"日期格式不正确呀\n例如:05-02")
#     # 查询此人绑定的直播间
#     pd.query(Config(id=event))
#     # result = await danmaku_rank(current_date,)

async def search_user(username):
    return httpx.get('http://api.bilibili.com/x/web-interface/search/type', params={
        'keyword': username,
        'search_type': 'bili_user'
    }).json()['data']

query_danmaku = on_startswith('查询弹幕')


@query_danmaku.handle()
async def _(bot: Bot, event: Event):
    params = event.raw_message.split()
    del(params[0])
    # 验证参数个数
    if len(params) < 2:
        await query_danmaku.finish(F"参数格式不正确呀\n例如: 查询弹幕 永雏塔菲 2021-08-01")

    # 验证日期格式
    query_date = None
    try:
        query_date = parse(params[1])
    except:
        await query_danmaku.finish(F"日期格式不正确呀\n例如: 查询弹幕 永雏塔菲 2021-08-01")

    # 查找指定用户
    uid = params[0]
    res = await search_user(uid)
    if res['numResults'] == 0:
        await query_danmaku.finish(F"找不到用户[{uid}]")

    # 保存uid
    uid = res['result'][0]['mid']
    danmaku_list = await query_danmaku_list('22603245', query_date.strftime('%Y-%m-%d'), uid)
    if not len(danmaku_list):
        await query_danmaku.finish(F"找不到用户[{uid}]的弹幕数据")

    reply_message = F"{uid}的弹幕数据:\n"
    for danmaku in danmaku_list:
        reply_message += (danmaku['msg'] + '\n')

    await query_danmaku.finish(reply_message)