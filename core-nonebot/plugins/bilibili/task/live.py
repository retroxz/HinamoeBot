#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author     :retroxz
@Date       :2021/11/10 22:19
@file       :live.py
@GitHub     :https://github.com/retroxz
"""

from nonebot import require
from ..model.subscribe import query_subscribe
from ..model.live_push_log import query_last_push_log, add_live_start_push_log, add_live_end_push_log
from ..api.live import get_live_status_by_uids
from ..utils.push_manager import generate_live_start_message, generate_live_end_message
from utils import send_message

scheduler = require("nonebot_plugin_apscheduler").scheduler


@scheduler.scheduled_job('interval', seconds=30)
async def get_live_status_task():
    sub_data = {}
    raws = await query_subscribe()
    for raw in raws:
        if not sub_data.get(raw['bili_uid']):
            sub_data[raw['bili_uid']] = []
        sub_data[raw['bili_uid']].append({
            'qid': raw['qid'],
            'qtype': raw['qtype'],
            'qname': raw['qname'],
            'at_all': raw['at_all']
        })
    sub_uids = list(sub_data.keys())
    live_status_list = list((await get_live_status_by_uids(sub_uids)).values())
    for live in live_status_list:
        # 检测到下播
        if live['live_status'] in [0, 2]:
            for sub in sub_data[live['uid']]:
                last_push_log = await query_last_push_log(live['uid'], sub['qid'], sub['qtype'])
                # 存在推送记录 如果是开播 就推送本次下播
                if last_push_log and last_push_log[0]['live_status'] == 1:
                    # 构建下播推送字符串
                    message = await generate_live_end_message(live, last_push_log)
                    await send_message(message, sub['qid'], sub['qtype'])
                    # 写入下播记录
                    await create_live_push_log(sub, live)

        # 检测到开播
        elif live['live_status'] == 1:
            for sub in sub_data[live['uid']]:
                last_push_log = (await query_last_push_log(live['uid'], sub['qid'], sub['qtype']))
                # 没有推送记录 是第一次订阅 推送本次开播
                if not last_push_log or last_push_log[0]['live_status'] == 0:
                    # 构建直播推送字符串
                    message = await generate_live_start_message(sub, live)
                    await send_message(message, sub['qid'], sub['qtype'])
                    # 写入开播记录
                    await create_live_push_log(sub, live)


async def create_live_push_log(sub, live):
    """
    写入直播推送日志
    :param sub: 直播订阅信息
    :param live: 直播间信息
    :return:
    """
    if live['live_status'] == 1:
        await add_live_start_push_log(**{
            'qid': sub['qid'],
            'qname': sub['qname'],
            'qtype': sub['qtype'],
            'bili_uid': live['uid'],
            'bili_room_id': live['room_id'],
            'bili_nick_name': live['uname'],
            'create_time': live['live_time'],
            'live_title': live['title'],
            'live_cover': live['cover_from_user']
        })
    elif live['live_status'] in [0, 2]:
        await add_live_end_push_log(**{
            'qid': sub['qid'],
            'qname': sub['qname'],
            'qtype': sub['qtype'],
            'bili_uid': live['uid'],
            'bili_room_id': live['room_id'],
            'bili_nick_name': live['uname']
        })
