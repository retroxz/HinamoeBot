#!/usr/bin/env python
# -*-coding:utf-8 -*-
from utils.base_config import BasePluginConfig


# 最新的推送时间
class Pushed(BasePluginConfig):
    def __init__(self, pushed_date):
        self.pushed_date = pushed_date


# 推送群
class PushGroup(BasePluginConfig):
    def __init__(self, group_id, room_id):
        self.group_id = group_id
        self.room_id = room_id

