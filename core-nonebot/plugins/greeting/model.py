# !/usr/bin/env python3
# coding=utf-8

from datetime import datetime
from utils.db import db_query
from dateutil.relativedelta import *


def get_start_date():
    current_date = datetime.now()
    if current_date.hour < 6:
        # 六点之前 算作前一天
        current_date = current_date + relativedelta(days=-1)
    return F"{current_date.strftime('%Y-%m-%d')} 06:00:00"


def get_end_date():
    current_date = datetime.now()
    if current_date.hour >= 6:
        current_date = current_date + relativedelta(days=1)
    return F"{current_date.strftime('%Y-%m-%d')} 05:59:59"


async def query_greeting_log(group_id, sender_id, type):
    sql = F"""
        SELECT * FROM bot.greeting_log WHERE create_time BETWEEN '{get_start_date()}' AND '{get_end_date()}'
        AND  group_id='{group_id}' AND sender_id='{sender_id}' AND type='{type}'
        ORDER BY create_time DESC 
        """
    return await db_query(sql)


async def add_greeting_log(group_id, group_name, sender_id, sender_name, type, morning_time, create_time):
    select_sql = F"""
        SELECT COUNT(*) AS `rank` FROM bot.greeting_log WHERE create_time between '{get_start_date()}' AND '{get_end_date()}' 
                       AND group_id='{group_id}' AND type='{type}'
    """
    rank = (await db_query(select_sql))[0]['rank']
    sql = F"""
        INSERT INTO bot.greeting_log
        (group_id, group_name, sender_id, sender_name, type, morning_time, create_time, `rank`) 
        VALUES ('{group_id}','{group_name}','{sender_id}','{sender_name}','{type}','{morning_time}',
            '{create_time}','{rank + 1}')
    """
    try:
        await db_query(sql)
    except:
        # 捕获到异常 修改QQ群名为默认名称
        group_name = 'QQ群'
        sender_name = 'QQ昵称'
        sql = F"""
               INSERT INTO bot.greeting_log
               (group_id, group_name, sender_id, sender_name, type, morning_time, create_time, `rank`) 
               VALUES ('{group_id}','{group_name}','{sender_id}','{sender_name}','{type}','{morning_time}',
                    '{create_time}','{rank + 1}')
           """
        await db_query(sql)
    return rank + 1
