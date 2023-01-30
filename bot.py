#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import nonebot
from utils.utils import load_plugins, init_data_dir, print_copy_right
from nonebot.adapters.onebot.v11.adapter import Adapter

nonebot.init()
app = nonebot.get_asgi()
driver = nonebot.get_driver()
driver.register_adapter(Adapter)

# 加载插件和配置
print_copy_right()
init_data_dir()
load_plugins()

if __name__ == "__main__":
    nonebot.run(app="__mp_main__:app")
