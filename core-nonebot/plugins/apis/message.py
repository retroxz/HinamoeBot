#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
@Author         : retroxz
@Date           : 2021/6/29 23:36
@Description    : None
@GitHub         : https://github.com/retroxz
"""
__author__ = "retroxz"

import nonebot
import inspect
from fastapi import FastAPI
from pydantic import BaseModel
from nonebot.adapters.cqhttp import Message

global_config = nonebot.get_driver().config
app: FastAPI = nonebot.get_driver().server_app


class Item(BaseModel):
    key: str
    message_type: str
    qid: int
    message: str


@app.post('/api/message/send')
async def _(item: Item):
    if not item.key == global_config.api_key:
        return {'code': 1, 'message': 'key无效'}
    # 获取bot实例
    try:
        bot = list(nonebot.get_bots().values())[0]
    except:
        return {'code': 1, 'message': 'Bot不在线'}
    params = {
        'message': Message(inspect.cleandoc(item.message)),
        'user_id' if item.message_type == 'private' else 'group_id': item.qid
    }
    await bot.call_api(F"send_{item.message_type}_msg", **params)
    return {'code': 0, 'message': '发送成功'}
