#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from utils import load_plugins, init_data_dir, print_copy_right
import nonebot
from nonebot.adapters.cqhttp import Bot as CQHTTPBot

nonebot.init()
app = nonebot.get_asgi()
driver = nonebot.get_driver()
driver.register_adapter("cqhttp", CQHTTPBot)

print_copy_right()
init_data_dir()
load_plugins()



if __name__ == "__main__":
    nonebot.run(app="__mp_main__:app")
