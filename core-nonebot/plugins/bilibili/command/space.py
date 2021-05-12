# !/usr/bin/env python3
# coding=utf-8

"""
    Bili user space commands
"""

from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, Event, MessageSegment, Message
from ..api.Space import Space
from ..exception import BiliUserNotFoundException
import inspect


uid_info = on_command('uid')


@uid_info.handle()
async def _(bot: Bot, event: Event):

    uid = event.get_message().__str__()
    try:
        user_space_data = await Space().uid_info(uid)
        print(user_space_data)
        reply_msg = F"""
        {MessageSegment.image(user_space_data['face'])}
            uid: {user_space_data['mid']}
            昵称: {user_space_data['name']}
            性别: {user_space_data['sex']}
            签名: {user_space_data['sign']}
            等级: {user_space_data['level']}
            生日: {user_space_data['birthday']}
            主页: https://space.bilibili.com/{user_space_data['mid']}
            直播间: {user_space_data['live_room']['url']}"""

        # reply_msg_dict = {
        #     'uid': user_space_data['mid'],
        #     '昵称': user_space_data['name'],
        #     '性别': user_space_data['sex'],
        #     '签名': user_space_data['sign'],
        #     '等级': user_space_data['level'],
        #     '生日': user_space_data['birthday'],
        #     '主页': f"https://space.bilibili.com/{user_space_data['mid']}",
        #     '直播间': user_space_data['live_room']['url']
        # }
        # reply_msg = f"{MessageSegment.image(user_space_data['face'])}\n"
        # reply_msg += "\n".join([f"	{key}: {value}" for key, value in reply_msg_dict])
        await uid_info.send(Message(inspect.cleandoc(reply_msg)))

    except BiliUserNotFoundException as e:
        await uid_info.send(e.__str__())
