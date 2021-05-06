#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

import nonebot
from nonebot.adapters.cqhttp import Bot as CQHTTPBot
from utils.plugin_data import PLUGINS_DATA_DIR

# 初始化
nonebot.init()
# 加载协议
driver = nonebot.get_driver()
driver.register_adapter("cqhttp", CQHTTPBot)  # 使用go-cqhttp

# 加载插件
nonebot.load_plugin("plugins.mute")

if __name__ == "__main__":
    # 初始化配置文件夹
    if not os.path.exists(PLUGINS_DATA_DIR):
        os.makedirs(PLUGINS_DATA_DIR)
    app = nonebot.get_asgi()
    # nonebot.run(app="__mp_main__:app")
    nonebot.run()
