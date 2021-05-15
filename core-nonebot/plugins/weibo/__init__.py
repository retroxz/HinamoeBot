#!/usr/bin/env python
# -*-coding:utf-8 -*-
import nonebot
from nonebot import on_command
from nonebot.adapters.cqhttp import GroupMessageEvent
from nonebot.permission import SUPERUSER
from nonebot.plugin import require
from nonebot.adapters import Bot
from nonebot.typing import T_State
from utils.plugin_data import Plugin_Data
from utils.db import db_query
import inspect


# Todo 以后再优化
PLUGIN_NAME = 'weibo'
pd = Plugin_Data(PLUGIN_NAME)


class Pushed:
    def __init__(self, pushed_date):
        self.pushed_date = pushed_date


class PushGroup:
    def __init__(self, id):
        self.id = id


async def push_wb():
    last_push_date = '1970-01-01'
    push_log = pd.db.table('Pushed').all()
    if push_log:
        last_push_date = push_log[0]['pushed_date']
    # 查询数据库
    sql = F"SELECT * FROM weibo.weibo WHERE publish_time > '{last_push_date}' ORDER BY publish_time DESC"
    res = await db_query(sql)
    if res:
        pd.db.table('Pushed').truncate()
        pd.add(Pushed(str(res[0]['publish_time'])))
    # 获取要推送的群
    push_group_list = pd.db.table('PushGroup').all()
    await send_wb_message(push_group_list,res)


async def send_wb_message(push_group_list, wb_list):
    # 推送
    bot = list(nonebot.get_bots().values())[0]
    for item in wb_list:
        push_wb_message = F"""
            发新微博啦！！
            发布时间: {item['publish_time']}
            微博正文: {item['content']}
            传送门: https://weibo.com/{item['user_id']}/{item['id']}
            """
        if push_group_list:
            for group in push_group_list:
                await bot.call_api('send_group_msg', group_id=group['id'], message=inspect.cleandoc(push_wb_message))


scheduler = require('nonebot_plugin_apscheduler').scheduler

scheduler.add_job(push_wb, "interval", seconds=30, id="xxx")

wb_push_on = on_command('开启微博推送', permission=SUPERUSER)


@wb_push_on.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    group_result = pd.query(PushGroup(event.group_id))
    if not group_result:
        pd.add(PushGroup(event.group_id))
        await wb_push_on.send(F'已开启本群微博推送')
        # 推送最新的一条
        sql = F"SELECT * FROM weibo.weibo ORDER BY publish_time DESC LIMIT 1"
        res = await db_query(sql)
        await send_wb_message([{"id": event.group_id}], res)
    else:
        await wb_push_on.send(F'已开启本群微博推送')

wb_push_off = on_command('关闭微博推送', permission=SUPERUSER)


@wb_push_off.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    group_result = pd.query(PushGroup(event.group_id))
    if group_result:
        pd.delete(PushGroup(event.group_id))
    await wb_push_off.finish(F'已关闭本群微博推送')
