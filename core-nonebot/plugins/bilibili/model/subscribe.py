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
from plugins.bilibili.api.Space import get_user_space_info


async def create_subscribe(event, uid, room_id):
    sql = F"""
        INSERT INTO `bot`.`bili_subscribes` 
        (`qid`, `qname`, `qtype`, `bili_uid`, `bili_room_id`, `bili_nick_name`, `operator_id`, `operator_name`)
        VALUES
        (%s,%s,%s,%s,%s,%s,%s,%s);    
        """

    # 获取事件类型和群号
    qtype, qid = get_event_id_and_type(event)
    info = await get_group_info(qid)
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


async def query_subscribe(event, uid):
    """
    查询订阅列表
    :param event:
    :param uid:
    :return:
    """
    sql = F"SELECT id,qid,qname,qtype,bili_uid,bili_room_id FROM bot.bili_subscribes " \
          F"WHERE bili_uid=%s AND qtype=%s AND qid=%s"
    # 获取事件类型和群号
    qtype, qid = get_event_id_and_type(event)
    # 查询数据库
    return await db_query(sql, [uid, qtype, qid])
