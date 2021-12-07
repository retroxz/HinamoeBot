# !/usr/bin/env python3
# coding=utf-8
import datetime

from nonebot import on_startswith
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from nonebot.adapters import Bot, Event
from .model import *
from utils import Plugin_Data
from .config import *
import httpx
from utils.config import Config


PLUGIN_NAME = 'danmaku'
DEFAULT_ROOM_ID = Config.danmaku['default_roomid']
pd = Plugin_Data(PLUGIN_NAME)
RANK_SIZE = Config.danmaku['rank_size']


danmaku_rank = on_startswith('弹幕排行')


@danmaku_rank.handle()
async def _(bot: Bot, event: Event):
    current_date = datetime.now()
    try:
        if event.raw_message.split('弹幕排行')[1]:
            current_date = parse(event.raw_message.split('弹幕排行')[-1])
    except:
        await danmaku_rank.finish(F"日期格式不正确呀\n例如:05-02")

    result = await queryDanmakuRankByDate(DEFAULT_ROOM_ID, current_date)
    reply_message = F"{current_date.strftime('%Y-%m-%d')} 弹幕TOP{RANK_SIZE}\n"
    if len(result) > 0:
        index = 1
        for raw in result:
            reply_message = reply_message + F"{index}. {raw['uname']}: {raw['danmaku']}\n"
            index = index + 1
    await danmaku_rank.finish(reply_message)


async def search_user(username):
    return httpx.get('http://api.bilibili.com/x/web-interface/search/type', params={
        'keyword': username,
        'search_type': 'bili_user'
    }).json()['data']


async def validate_data(raws, date):
    index = 0
    for raw in raws:
        if raw['timestamp'] > int(date.timestamp() * 1000):
            break
        index += 1
    return raws[:index]

query_danmaku = on_startswith('查询弹幕')


@query_danmaku.handle()
async def _(bot: Bot, event: Event):
    params = event.raw_message.split()
    del(params[0])
    # 验证参数
    if len(params) < 2:
        await query_danmaku.finish(F"参数格式不正确呀\n例如: 查询弹幕 永雏塔菲 2021-08-01 2(可选)")

    # 验证日期格式
    query_date = None
    try:
        # 转换日期格式
        params[1].replace('.', '')
        params[1].replace('-', '')
        params[1].replace('/', '')
        if len(params[1]) == 4:
            params[1] = F"{datetime.now().year}{params[1]}"
        query_date = parse(params[1])
        if query_date.year < 2000:
            raise Exception
    except:
        await query_danmaku.finish(F"日期格式不正确呀\n例如: 查询弹幕 永雏塔菲 2021-08-01 2")

    # 查找指定用户
    username= params[0]
    res = await search_user(username)
    if res['numResults'] == 0:
        await query_danmaku.finish(F"找不到用户[{username}]")
    # 保存uid
    uid = res['result'][0]['mid']

    # 查询数据
    page = 1 if len(params) == 2 else params[2]
    danmaku_list = await query_danmaku_list(DEFAULT_ROOM_ID, query_date.strftime('%Y-%m-%d'), uid, page)
    # 过滤数据
    query_date = query_date + relativedelta(days=1)
    danmaku_list = await validate_data(danmaku_list, query_date)
    query_date = query_date - relativedelta(days=1)
    if not len(danmaku_list):
        await query_danmaku.finish(F"找不到{query_date.strftime('%Y年%m月%d日')}用户[{username}]的弹幕数据")

    # 构造返回
    index = 1
    reply_message = F"{query_date.strftime('%Y年%m月%d日')}{username}的弹幕数据:\n"
    for danmaku in danmaku_list:
        reply_message += F"{index}. {danmaku['msg']}\n"
        index += 1

    await query_danmaku.finish(reply_message)