#!/usr/bin/env python
# -*-coding:utf-8 -*-
import nonebot
from nonebot import on_command
from nonebot.adapters.cqhttp import MessageSegment, Message, MessageEvent
from nonebot.plugin import require
from nonebot.adapters import Bot
from nonebot.typing import T_State
from utils.plugin_data import Plugin_Data
from utils.db import db_query
from utils import is_admin
import inspect
from .config import *

# Todo 以后再优化
PLUGIN_NAME = 'weibo'
pd = Plugin_Data(PLUGIN_NAME)


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
    await send_wb_message(push_group_list, res)


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
        if item['original_pictures']:
            origin_pics = item['original_pictures'].split(',')
            for pic in origin_pics:
                push_wb_message += F"{MessageSegment.image(file=pic)}"

        for group in push_group_list:
            # 检查推送记录
            if not group.get('pushed_log'):
                group['pushed_log'] = []
            if item['id'] not in group['pushed_log']:
                params = {
                    'message': Message(inspect.cleandoc(push_wb_message)),
                    'user_id' if group['type'] == 'private' else 'group_id': group['id']
                }
                await bot.call_api(F"send_{group['type']}_msg", **params)
                # 记录推送日志
                group['pushed_log'].append(item['id'])
                pd.update(
                    PushGroup(pushed_log=group['pushed_log']),
                    PushGroup(id=group['id']))


scheduler = require('nonebot_plugin_apscheduler').scheduler

scheduler.add_job(push_wb, "interval", seconds=20, id="xxx")

wb_push_on = on_command('开启微博推送')


@wb_push_on.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    if not is_admin(bot,event): return
    if event.message_type == 'private':
        # 私聊消息
        query_group = PushGroup(id=event.user_id, type=event.message_type)
    else:
        query_group = PushGroup(id=event.group_id, type=event.message_type)
    result = pd.query(query_group)
    if not result:
        pd.add(query_group)
    await wb_push_on.send(F'已开启微博推送')


wb_push_off = on_command('关闭微博推送')


@wb_push_off.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    if not is_admin(bot,event): return
    if event.message_type == 'private':
        # 私聊消息
        query_group = PushGroup(id=event.user_id, type=event.message_type)
    else:
        query_group = PushGroup(id=event.group_id, type=event.message_type)
    result = pd.query(query_group)
    if result:
        pd.delete(query_group)
    await wb_push_off.finish(F'已关闭微博推送')
