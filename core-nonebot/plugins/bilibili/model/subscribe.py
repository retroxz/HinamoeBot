#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
@Author         : retroxz
@Date           : 2021/9/23 19:03
@Description    : None
@GitHub         : https://github.com/retroxz
"""
__author__ = "retroxz"

import emoji
from utils.db import db_query
from utils import get_event_id_and_type, get_group_info, filter_emoji
from plugins.bilibili.api.space import get_user_space_info


async def create_subscribe(event, uid, room_id):
    """
    添加新订阅
    :param event:
    :param uid:
    :param room_id:
    :return:
    """
    sql = F"""
        INSERT INTO `bot`.`bili_subscribes` 
        (`qid`, `qname`, `qtype`, `bili_uid`, `bili_room_id`, `bili_nick_name`, `operator_id`, `operator_name`)
        VALUES
        (%s,%s,%s,%s,%s,%s,%s,%s);    
        """

    # 获取事件类型和群号
    qtype, qid = get_event_id_and_type(event)
    qname = ''
    if qtype == 'group':
        info = await get_group_info(qid)
        qname = info['group_name']
    else:
        qname = event.sender.nickname
    space_info = await get_user_space_info(uid)

    # 写入
    raws = await db_query(sql, [qid, filter_emoji(qname), qtype, uid, room_id, space_info['name'],
                                event.sender.user_id, filter_emoji(event.sender.nickname)])
    return raws


async def query_subscribe(event=None, uid=None):
    """
    查询订阅列表
    :param event:
    :param uid:
    :return:
    """

    # 获取事件类型和群号
    if event is None:
        sql = 'SELECT qid,qname,qtype,at_all,bili_uid,bili_room_id FROM  bot.bili_subscribes'
        return await db_query(sql)
    elif uid is None:
        qtype, qid = get_event_id_and_type(event)
        sql = F"SELECT id,qid,qname,qtype,bili_uid,bili_room_id,bili_nick_name,at_all FROM bot.bili_subscribes " \
              F"WHERE qtype=%s AND qid=%s"
        return await db_query(sql, [qtype, qid])
    else:
        qtype, qid = get_event_id_and_type(event)
        sql = F"SELECT id,qid,qname,qtype,bili_uid,bili_room_id,bili_nick_name,at_all FROM bot.bili_subscribes " \
              F"WHERE bili_uid=%s AND qtype=%s AND qid=%s"
        # 查询数据库
        return await db_query(sql, [uid, qtype, qid])


async def delete_subscribe(event, uid):
    """
    删除订阅
    :param event:
    :param uid:
    :return:
    """
    sql = "DELETE FROM bot.bili_subscribes WHERE bili_uid=%s AND qtype=%s AND qid=%s"
    # 获取事件类型和群号
    qtype, qid = get_event_id_and_type(event)
    # 删除
    return await db_query(sql, [uid, qtype, qid])


async def update_subscribe_at_all(event, uid, is_at_all):
    # 获取事件类型和群号
    qtype, qid = get_event_id_and_type(event)

    is_at_all = 1 if is_at_all else 0
    sql = "UPDATE bot.bili_subscribes SET at_all=%s WHERE bili_uid=%s AND qtype=%s AND qid=%s"

    # 更新
    return await db_query(sql, [is_at_all, uid, qtype, qid])
