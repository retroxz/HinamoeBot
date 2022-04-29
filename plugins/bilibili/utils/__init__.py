#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
@Author         : retroxz
@Date           : 2021/9/24 21:46
@Description    : None
@GitHub         : https://github.com/retroxz
"""
__author__ = "retroxz"


def filter_subscribes(subscribes):
    result = {}
    for subscribe in subscribes:
        if not result.get(subscribe['bili_uid']):
            result[subscribe['bili_uid']] = []
        result[subscribe['bili_uid']].append({
            'id': subscribe['id'],
            'qid': subscribe['qid'],
            'qtype': subscribe['qtype'],
            'qname': subscribe['qname'],
            'at_all': subscribe['at_all'],
            'last_dynamic_id': subscribe['last_dynamic_id'],
            'last_dynamic_time': subscribe['last_dynamic_time']
        })
    return result
