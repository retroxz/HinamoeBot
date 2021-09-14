# !/usr/bin/env python3
# coding=utf-8


"""
    插件内部数据管理
"""
from tinydb import TinyDB, Query

PLUGINS_DATA_DIR = './data/plugins/'


class Plugin_Data:
    def __init__(self, plugin_name):
        self.db = TinyDB(F"{PLUGINS_DATA_DIR}{plugin_name}.json")

    def add(self, row):
        return self.db.table(row.__class__.__name__).insert(dict(row))

    def query(self, query_dict):
        return self.db.table(query_dict.__class__.__name__).search(
            Query().fragment(dict(query_dict)))

    def delete(self, remove_dict):
        return self.db.table(remove_dict.__class__.__name__).remove(
            Query().fragment(dict(remove_dict)))

    def update(self, update, query):
        return self.db.table(query.__class__.__name__).update(dict(update), Query().fragment(dict(query)))
