# !/usr/bin/env python3
# coding=utf-8

"""
    Bili user space commands
"""

from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, Event, MessageSegment, Message
from ..service.space import get_user_info
from ..exception import BiliUserNotFoundException
import inspect


uid_info = on_command('uid')


@uid_info.handle()
async def _(bot: Bot, event: Event):

    uid = event.get_message().__str__()
    try:
        user_space_data = await get_user_info(uid)
        reply_msg = F"""
        {MessageSegment.image(user_space_data['face'])}
        uid: {user_space_data['mid']}
        昵称: {user_space_data['name']}
        性别: {user_space_data['sex']}
        签名: {user_space_data['sign']}
        粉丝数: {user_space_data['fans']}
        主页: https://space.bilibili.com/{user_space_data['mid']}
        直播间: https://live.bilibili.com/{user_space_data['roomid']}
        """
        await uid_info.finish(Message(inspect.cleandoc(reply_msg)))

    except BiliUserNotFoundException as e:
        await uid_info.finish(e.__str__())
