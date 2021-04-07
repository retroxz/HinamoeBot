#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nonebot
from nonebot.adapters.cqhttp import Bot as CQHTTPBot

# Custom your logger
# 
# from nonebot.log import logger, default_format
# logger.add("error.log",
#            rotation="00:00",
#            diagnose=False,
#            level="ERROR",
#            format=default_format)

# You can pass some keyword args config to init function
nonebot.init()

driver = nonebot.get_driver()
driver.register_adapter("cqhttp", CQHTTPBot)  # 使用go-cqhttp

# 加载插件
nonebot.load_builtin_plugins()
nonebot.load_plugins("hina/plugins")
nonebot.load_from_toml("pyproject.toml")

app = nonebot.get_asgi()

# Modify some config / config depends on loaded configs
# 
# config = driver.config
# do something...


if __name__ == "__main__":
    nonebot.run(app="__mp_main__:app")
