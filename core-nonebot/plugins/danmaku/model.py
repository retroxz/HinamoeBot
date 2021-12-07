# !/usr/bin/env python3
# coding=utf-8
from datetime import datetime
from utils.db import db_query
from utils.config import Config
PAGE_SIZE = Config.danmaku['page_size']
RANK_SIZE = Config.danmaku['rank_size']


async def queryDanmakuRankByDate(room_id, current_date=datetime.now()):
    sql = F"""
            SELECT uname, COUNT(*) AS 'danmaku' FROM bili.bili_danmaku 
                WHERE timestamp > UNIX_TIMESTAMP('{current_date.strftime('%Y-%m-%d')} 00:00:00')* 1000 
                AND timestamp < UNIX_TIMESTAMP( '{current_date.strftime('%Y-%m-%d')} 23:59:59' )* 1000 
                AND room_id={room_id} GROUP BY uid ORDER BY danmaku DESC LIMIT {RANK_SIZE}
        """

    return await db_query(sql)


async def query_danmaku_list(room_id, query_date, uid, page=1):
    page_offset = 0 if page == 1 else (int(page) - 1) * PAGE_SIZE - 1
    sql = "SELECT DISTINCT msg,timestamp FROM bili.bili_danmaku WHERE timestamp > UNIX_TIMESTAMP(%s)*1000 " \
          "AND room_id = %s AND uid = %s ORDER BY timestamp LIMIT %s,%s"

    return await db_query(sql, (query_date, room_id, uid, page_offset, PAGE_SIZE))
