#!/usr/bin/env python
# -*-coding:utf-8 -*-
from utils.base_config import BasePluginConfig


# 最新的推送时间
class Pushed(BasePluginConfig):
    def __init__(self, pushed_date):
        self.pushed_date = pushed_date


# 推送群
class PushGroup(BasePluginConfig):
    def __init__(self, id=None, pushed_log=None, type=''):
        if pushed_log is None:
            pushed_log = []
        self.pushed_log = pushed_log
        self.id = id
        self.type = type
