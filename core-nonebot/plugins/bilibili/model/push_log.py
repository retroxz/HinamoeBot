#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author     :retroxz
@Date       :2021/11/10 23:58
@file       :push_log.py
@GitHub     :https://github.com/retroxz
"""


from utils.db import db_query


async def query_live_on_push_log(uid, create_time):
    """
    查询直播推送记录
    :param uid: 主播uid
    :param create_time: 直播开始时间
    :return:
    """
    sql = F"SELECT qid FROM bot.bili_push_log WHERE bili_uid={uid} AND create_time={create_time} AND sub_type=2"
    return await db_query(sql)
