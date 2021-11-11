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
from ..model.live_push_log import query_last_push_log
from ..api.live import get_live_status_by_uids

scheduler = require("nonebot_plugin_apscheduler").scheduler


async def get_live_status_task():
    sub_data = {}
    raws = await query_subscribe()
    for raw in raws:
        if not sub_data.get(raw['bili_uid']):
            sub_data[raw['bili_uid']] = []
        sub_data[raw['bili_uid']].append({
            'qid': raw['qid'],
            'qtype': raw['qtype'],
            'qname': raw['qname']
        })
    sub_uids = list(sub_data.keys())
    print(sub_uids)
    live_status_list = list((await get_live_status_by_uids(sub_uids)).values())
    print(live_status_list)
    for live in live_status_list:
        if live['live_status'] in [0, 2]:
            for sub in sub_data[live['uid']]:
                last_push_log = await query_last_push_log(live['uid'], sub['qid'], sub['qtype'])
                # 没有推送记录 是第一次订阅 不推送下播
                if not last_push_log:
                    print('第一次订阅 不推送下播')
                    continue
                # 存在推送记录 如果是开播 就推送本次下播
                if last_push_log['live_status'] == 1:
                    print('推送下播')
        elif live['live_status'] == 1:
            for sub in sub_data[live['uid']]:
                last_push_log = await query_last_push_log(live['uid'], sub['qid'], sub['qtype'])
                # 没有推送记录 是第一次订阅 推送本次开播
                if not last_push_log:
                    print('推送开播')
                # 存在推送记录 如果是下播 就推送本次开播
                if last_push_log['live_status'] == 0:
                    print('推送开播')


async def create_live_push_log(sub, live, status):
    pass



