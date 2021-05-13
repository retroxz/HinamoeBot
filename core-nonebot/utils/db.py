# !/usr/bin/env python3
# coding=utf-8

import nonebot
import aiomysql

global_config = nonebot.get_driver().config


async def db_query(sql: str, params=tuple()):
    conn = await aiomysql.connect(host=global_config.db_host, port=global_config.db_port,
                                  user=global_config.db_username, password=global_config.db_password, db='mysql',
                                  echo=True, autocommit=True)

    cur = await conn.cursor(aiomysql.DictCursor)
    await cur.execute(sql, params)
    r = await cur.fetchall()
    await cur.close()
    conn.close()
    return r
