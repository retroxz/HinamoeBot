# !/usr/bin/env python3
# coding=utf-8

"""
    Bili user space commands
"""

from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, Event, MessageSegment, Message
from ..api.Space import get_user_space_info, get_user_card_info
from ..api.Search import search_user_uid
from ..exception import BiliUserNotFoundException
import inspect


uid_info = on_command('uid')


@uid_info.handle()
async def _(bot: Bot, event: Event):

    uid = event.get_message().__str__()
    try:
        uid = await search_user_uid(uid)
        user_space_data = await get_user_space_info(uid)
        user_card_data = await get_user_card_info(uid)
        reply_msg = F"""{MessageSegment.image(user_space_data['face'])}
        uid: {user_space_data['mid']}
        昵称: {user_space_data['name']}
        签名: {user_space_data['sign']}
        等级: {user_space_data['level']}
        粉丝数: {user_card_data['follower']}
        生日: {user_space_data['birthday']}
        主页: https://space.bilibili.com/{user_space_data['mid']}
        直播间: {user_space_data['live_room']['url']}"""
        await uid_info.send(Message(inspect.cleandoc(reply_msg)))

    except BiliUserNotFoundException as e:
        await uid_info.send(e.__str__())
