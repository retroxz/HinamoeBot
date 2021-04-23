# !/usr/bin/env python3
# coding=utf-8


"""
    插件内部数据管理
"""
from tinydb import TinyDB, Query
import os
from .logger import info, warning, error

PLUGINS_DATA_DIR = './data/plugins/'


class Plugin_Data:
    def __init__(self, plugin_name):
        self.db = TinyDB(F"{PLUGINS_DATA_DIR}{plugin_name}.json")

    def add(self, row):
        return self.db.table(row.__class__.__name__).insert(row.__dict__)

    def query(self, query_dict):
        return self.db.table(query_dict.__class__.__name__).search(
            Query().fragment(query_dict.__dict__))

    def delete(self, remove_dict):
        return self.db.table(remove_dict.__class__.__name__).remove(
            Query().fragment(remove_dict.__dict__))

