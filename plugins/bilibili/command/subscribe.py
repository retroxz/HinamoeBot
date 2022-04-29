# -*- coding: utf-8 -*-
# @Time    : 2021/9/23 16:39
# @Author  : retroxz
# @Email   : zzxee666@gmail.com
# @File    : subscribe.py

__author__ = "retroxz"

import inspect
from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent, PrivateMessageEvent
from utils import is_admin, bot_is_admin
from plugins.bilibili.api.search import search_user_uid
from plugins.bilibili.exception import BiliUserNotFoundException
from plugins.bilibili.model.subscribe import *

# 新增订阅
add_subscribe = on_command('新增订阅')

# 删除订阅
del_subscribe = on_command('取消订阅')

# 查看订阅
show_subscribe = on_command('查看订阅')

# 艾特全体
enable_at_all = on_command('打开全体')

# 关闭全体
disable_at_all = on_command('关闭全体')


@add_subscribe.handle()
async def _(bot: Bot, event: PrivateMessageEvent):
    """
    新增订阅 私聊
    :param bot:
    :param event:
    :return:
    """
    print(event)


@add_subscribe.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    """
    新增订阅 群聊
    :param bot:
    :param event:
    :return:
    """

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


@del_subscribe.handle()
async def _(bot: Bot, event: PrivateMessageEvent):
    pass


@del_subscribe.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    """

    :param bot:
    :param event:
    :return:
    """
    # 只有管理员和超管可以使用
    global uid, room_id
    if not is_admin(event, bot):
        await del_subscribe.finish('呜呜呜 只有管理员可以编辑群订阅信息')
    if not len(event.message):
        await del_subscribe.finish('不知道要删除谁')

    # 获取订阅用户的uid
    try:
        uid, room_id = await search_user_uid(str(event.message[0]))
    except BiliUserNotFoundException as e:
        await del_subscribe.finish(e.message())

    # 删除订阅
    res = await delete_subscribe(event, uid)
    await add_subscribe.finish(F"已取消订阅{str(event.message[0])}直播和动态!")


@show_subscribe.handle()
async def _(bot: Bot, event: PrivateMessageEvent):
    pass


@show_subscribe.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    # 查询订阅列表
    subscribe_list = await query_subscribe(event)
    if not len(subscribe_list):
        await show_subscribe.finish('你群没有订阅信息')
    message = '你群订阅列表:\n'
    await show_subscribe.finish(inspect.cleandoc(message + generate_subscribe_list(subscribe_list)))


def generate_subscribe_list(subscribe_list):
    message_raw = ''
    index = 1
    for subscribe in subscribe_list:
        message_raw += F"\t{index}. {subscribe['bili_nick_name']}({subscribe['bili_uid']}){'🎉艾特全体' if subscribe['at_all'] == 1 else ''}\n"
        index += 1
    return message_raw


@enable_at_all.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    # 本群没有订阅却开启了全体时的附加信息
    auto_add_subscribe = ''

    # 只有管理员和超管可以使用
    global uid, room_id
    if not is_admin(event, bot):
        await enable_at_all.finish('呜呜呜 只有管理员可以编辑群订阅信息')
    if not len(event.message):
        await enable_at_all.finish('需要告诉我打开谁的全体')

    # 查询bot是否有权限
    if not await bot_is_admin(event.group_id, bot):
        await enable_at_all.finish('我在这个群不是狗管理啊')

    # 获取订阅用户的uid
    try:
        uid, room_id = await search_user_uid(str(event.message[0]))
    except BiliUserNotFoundException as e:
        await enable_at_all.finish(e.message())

    # 查询本群是否订阅了该up
    subscribe_list = await query_subscribe(event, uid)
    if not len(subscribe_list):
        # 自动订阅
        await create_subscribe(event, uid, room_id)
        # 附加提示
        auto_add_subscribe = F"\n你群未订阅{str(event.message[0])}，不过我已经帮你订阅上了嘻嘻"

    # 更新艾特全体
    raw = await update_subscribe_at_all(event, uid, True)

    await enable_at_all.finish(F"开启成功！{str(event.message[0])}开播的时候会艾特全体哦！{auto_add_subscribe}")


@disable_at_all.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    # 只有管理员和超管可以使用
    global uid, room_id
    if not is_admin(event, bot):
        await disable_at_all.finish('呜呜呜 只有管理员可以编辑群订阅信息')
    if not len(event.message):
        await disable_at_all.finish('需要告诉我关闭谁的全体')

        # 获取订阅用户的uid
    try:
        uid, room_id = await search_user_uid(str(event.message[0]))
    except BiliUserNotFoundException as e:
        await disable_at_all.finish(e.message())

    # 更新艾特全体
    await update_subscribe_at_all(event, uid, False)

    await enable_at_all.finish(F"关闭成功！对{str(event.message[0])}的爱已经消失了吗")