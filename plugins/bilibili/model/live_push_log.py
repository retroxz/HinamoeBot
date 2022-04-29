#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author     :retroxz
@Date       :2021/11/10 23:58
@file       :live_push_log.py
@GitHub     :https://github.com/retroxz
"""

from utils.db import db_query


async def query_last_push_log(uid, qid, qtype):
    """
    查询某主播在某群的最近推送记录
    :param uid: 主播uid
    :param create_time: 直播开始时间
    :return:
    """
    sql = F"SELECT qid, live_status, create_time FROM bot.bili_live_push_log WHERE bili_uid={uid} AND qid={qid} AND qtype='{qtype}' " \
          F"ORDER BY id DESC LIMIT 1"
    return await db_query(sql)


async def add_live_start_push_log(qid, qname, qtype, bili_uid, bili_room_id, bili_nick_name, create_time,
                                  live_cover, live_title):

    sql = F"""
        INSERT INTO bot.bili_live_push_log (qid, qname, qtype, bili_uid, bili_room_id, bili_nick_name, create_time, live_cover, live_status, live_title)
        VALUES ({qid}, '{qname}', '{qtype}', {bili_uid}, {bili_room_id}, '{bili_nick_name}', {create_time}, '{live_cover}', 1, '{live_title}')
   """
    return await db_query(sql)


async def add_live_end_push_log(qid, qname, qtype, bili_uid, bili_room_id, bili_nick_name):
    sql = F"""
        INSERT INTO bot.bili_live_push_log (qid, qname, qtype, bili_uid, bili_room_id, bili_nick_name, live_status)
        VALUES ({qid}, '{qname}', '{qtype}', {bili_uid}, {bili_room_id}, '{bili_nick_name}', 0)
   """
    return await db_query(sql)

