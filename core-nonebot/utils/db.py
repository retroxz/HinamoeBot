# !/usr/bin/env python3
# coding=utf-8
import os
from functools import wraps

import nonebot
import aiomysql
from .logger import logger
from .config import Config
import inspect

global_config = nonebot.get_driver().config


async def db_query(sql: str, params=None, source='default'):
    """
    执行SQL语句
    :param source: 数据源
    :param sql: SQL语句
    :param params: 参数列表
    :return:
    """
    # 获取调用方插件名
    plugins_name = await load_data_source()

    if params is None:
        params = []
    # 加载数据库配置
    dbconfig = Config.get(F"{plugins_name}.datasource")
    if dbconfig is None:
        # 无自定义配置 使用默认配置
        dbconfig = Config.get('datasource')
        if dbconfig is None:
            # 不存在默认数据库连接
            # Todo 将默认数据库连接放到bot启动时进行检查
            logger.error(F"找不到默认的数据库连接! ")
            return
    conn = await aiomysql.connect(host=dbconfig.host, port=dbconfig.port,
                                  user=dbconfig.username, password=dbconfig.password, db='mysql',
                                  echo=True, autocommit=True)

    cur = await conn.cursor(aiomysql.DictCursor)
    await cur.execute(sql, tuple(params))
    r = await cur.fetchall()
    # 将执行过的SQL写入到日志中
    logger.success(F"执行SQL: {cur._last_executed}")
    await cur.close()
    conn.close()
    return r


async def load_data_source():
    """
    获取当前调用db函数的数据源 即插件包名
    :return:
    """
    # 获取到当前调用方
    frame = inspect.currentframe().f_back.f_back
    # 获取调用方全路径
    (full_path, ine_number, function_name, lines, index) = inspect.getframeinfo(frame)
    # 分割
    path_arr = str(full_path).split(os.sep)
    # 查找到plugins文件夹后的插件包名
    index = path_arr.index('plugins') + 1
    # 返回插件包名
    return path_arr[index]

