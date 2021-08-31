# !/usr/bin/env python3
# coding=utf-8
from datetime import datetime
from utils.db import db_query


async def queryDanmakuRankByDate(room_id, current_date=datetime.now()):
    sql = F"""
            SELECT uname AS '昵称',COUNT(*) AS '弹幕量' FROM bili_danmaku 
                WHERE timestamp > UNIX_TIMESTAMP('{current_date.strftime('%Y-%m-%d')} 00:00:00')* 1000 
                AND timestamp < UNIX_TIMESTAMP( '{current_date.strftime('%Y-%m-%d')} 23:59:59' )* 1000 
                AND room_id={room_id} GROUP BY uid ORDER BY 弹幕量 DESC LIMIT 10
        """
    return await db_query(sql)


async def query_danmaku_list(room_id, query_date, uid):
    sql = "SELECT DISTINCT msg FROM bili.bili_danmaku WHERE timestamp > UNIX_TIMESTAMP(%s)*1000 " \
          "AND room_id = %s AND uid = %s ORDER BY timestamp LIMIT 20 "

    return await db_query(sql, (query_date, room_id, uid))
