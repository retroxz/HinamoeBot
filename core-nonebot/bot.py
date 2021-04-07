#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nonebot
from nonebot.adapters.cqhttp import Bot as CQHTTPBot


# 初始化
nonebot.init()
# 加载协议
driver = nonebot.get_driver()
driver.register_adapter("cqhttp", CQHTTPBot)  # 使用go-cqhttp

# 加载插件
nonebot.load_builtin_plugins()
nonebot.load_plugins("hinamoe/plugins")

app = nonebot.get_asgi()


if __name__ == "__main__":
    nonebot.run(app="__mp_main__:app")
