#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
@Author         : retroxz
@Date           : 2021/9/27 0:20
@Description    : None
@GitHub         : https://github.com/retroxz
"""
__author__ = "retroxz"

from utils.db import db_query
import json


class auth_model:
    @classmethod
    async def update_cache(cls, cookies):
        cookies = json.dumps(cookies)
        cookies_list = await db_query(
            "SELECT * FROM bot.plugins_config WHERE plugin_name='bilibili' AND name='cookies'")
        if cookies_list:
            # 已存在 更新
            await db_query(
                F"UPDATE bot.plugins_config SET value=%s WHERE plugin_name='bilibili' AND name='cookies'", [cookies])
        else:
            # 不存在 插入
            await db_query(
                F"INSERT INTO bot.plugins_config (name,value,plugin_name) VALUES ('cookies',%s,'bilibili')", [cookies])

    @classmethod
    async def query_cache(cls):
        cookies_list = await db_query(
            "SELECT value FROM bot.plugins_config WHERE plugin_name='bilibili' AND name='cookies'")
        return json.loads(cookies_list[0]['value']) if cookies_list else {}
