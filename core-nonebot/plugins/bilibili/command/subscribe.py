# -*- coding: utf-8 -*-
# @Time    : 2021/9/23 16:39
# @Author  : retroxz
# @Email   : zzxee666@gmail.com
# @File    : subscribe.py

__author__ = "retroxz"

from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent, PrivateMessageEvent
from utils import is_admin
from plugins.bilibili.api.Search import search_user_uid
from plugins.bilibili.exception import BiliUserNotFoundException
from plugins.bilibili.model.subscribe import query_subscribe, create_subscribe

# 订阅

add_subscribe = on_command('新增订阅')

# 艾特全体
at_all = on_command('打开全体')


@add_subscribe.handle()
async def _(bot: Bot, event: PrivateMessageEvent):
    print(event)


@add_subscribe.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    # 只有管理员和超管可以使用
    global uid, room_id
    if not is_admin(event, bot):
        await add_subscribe.finish('呜呜呜 只有管理员可以编辑群订阅信息')
        return
    if not len(event.message):
        await add_subscribe.finish('要告诉我订阅谁呀')
        return

    # 获取订阅用户的uid
    try:
        uid, room_id = await search_user_uid(str(event.message[0]))
    except BiliUserNotFoundException as e:
        await add_subscribe.finish(e.message())

    # 查询是否有记录
    subscribe_list = await query_subscribe(event, uid)
    if len(subscribe_list):
        await add_subscribe.finish(F"订阅{str(event.message[0])}直播和动态成功!")
    # 写入一条新记录
    await create_subscribe(event, uid, room_id)
    await add_subscribe.finish(F"订阅{str(event.message[0])}直播和动态成功!")