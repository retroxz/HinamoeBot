# -*- coding: utf-8 -*-
# @Time    : 2021/12/30 11:03
# @Author  : retroxz
# @Email   : zzxee666@gmail.com
# @File    : dynamic.py

__author__ = "retroxz"

from ..model.subscribe import query_subscribe
from ..utils import filter_subscribes
from ..api.dynamic import get_new_dynamic
import json


async def get_new_dynamic_task():
    raws = await query_subscribe()
    sub_data = filter_subscribes(raws)
    print(sub_data)
    info = await get_new_dynamic('1265680561')
    origin = info['cards'][0]['desc']['origin']
    data = json.loads(info['cards'][0]['card'])
    data1 = json.loads(info['cards'][1]['card'])
    print(data)


