# !/usr/bin/env python3
# coding=utf-8
from utils.base_config import BasePluginConfig

class Config(BasePluginConfig):
    def __init__(self, id=0, room_id=0, type=0):
        self.id = id
        self.room_id = room_id,
        self.type = type

