# !/usr/bin/env python3
# coding=utf-8

import nonebot
import aiomysql
from .logger import logger

global_config = nonebot.get_driver().config


async def db_query(sql: str, params=None):
    """
    执行SQL语句
    :param sql: SQL语句
    :param params: 参数列表
    :return:
    """

    if params is None:
        params = []
    conn = await aiomysql.connect(host=global_config.db_host, port=global_config.db_port,
                                  user=global_config.db_username, password=global_config.db_password, db='mysql',
                                  echo=True, autocommit=True)

    cur = await conn.cursor(aiomysql.DictCursor)
    await cur.execute(sql, tuple(params))
    r = await cur.fetchall()
    # 将执行过的SQL写入到日志中
    logger.success(F"执行SQL: {cur._last_executed}")
    await cur.close()
    conn.close()
    return r
