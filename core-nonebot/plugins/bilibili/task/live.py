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
from ..model.push_log import query_live_on_push_log
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
            'qtype': raw['qtype']
        })
    sub_uids = list(sub_data.keys())
    print(sub_uids)
    live_status_list = list((await get_live_status_by_uids(sub_uids)).values())
    print(live_status_list)
    for live in live_status_list:
        if live['live_status'] == 1:
            # 查询开播推送记录
            push_log = list(await query_live_on_push_log(live['uid'], live['live_time']))
            for sub in sub_data[live['uid']]:
                print(sub)
                if sub['qid'] not in push_log:
                    # 推送
                    pass





