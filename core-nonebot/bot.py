#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from utils.plugin_data import PLUGINS_DATA_DIR
import nonebot
from nonebot.adapters.cqhttp import Bot as CQHTTPBot


nonebot.init()
app = nonebot.get_asgi()

driver = nonebot.get_driver()
driver.register_adapter("cqhttp", CQHTTPBot)

# 加载插件
nonebot.load_plugin("plugins.mute")
nonebot.load_plugin("plugins.weibo")
nonebot.load_plugin("plugins.fortune")
nonebot.load_plugin("plugins.danmaku")

if __name__ == "__main__":
    # 初始化配置文件夹
    if not os.path.exists(PLUGINS_DATA_DIR):
        os.makedirs(PLUGINS_DATA_DIR)
    nonebot.run(app="__mp_main__:app")
