# !/usr/bin/env python3
# coding=utf-8  
__author__ = 'retroxz'

import os
import nonebot
from utils.plugin_data import PLUGINS_DATA_DIR
from utils.config import Config
from colorama import init as colorInit

BOT_PATH = os.path.abspath(os.path.join(os.path.expanduser('~'), '.hinamoe/bot'))


def init_data_dir():
    """
    初始化数据目录
    :return:
    """
    if not os.path.exists(PLUGINS_DATA_DIR):
        os.makedirs(PLUGINS_DATA_DIR)


def load_plugins():
    """
    加载插件
    :return:
    """
    for plugin in Config.plugins:
        nonebot.load_plugin(F"plugins.{plugin}")


def print_copy_right():
    colorInit()
    COPYRIGHT = F"\033[0;37;1m" + f"""
  _    _ _                                  ____        _   
 | |  | (_)                                |  _ \      | |  
 | |__| |_ _ __   __ _ _ __ ___   ___   ___| |_) | ___ | |_ 
 |  __  | | '_ \ / _` | '_ ` _ \ / _ \ / _ \  _ < / _ \| __|
 | |  | | | | | | (_| | | | | | | (_) |  __/ |_) | (_) | |_ 
 |_|  |_|_|_| |_|\__,_|_| |_| |_|\___/ \___|____/ \___/ \__|   
 
Copyright © 2019-2021 HinamoeOfficial,All Rights Reserved
Project: https://github.com/retroxz/HinamoeBot
BOT数据目录: {BOT_PATH}                                                
""" + "\033[0m"
    print(COPYRIGHT)
