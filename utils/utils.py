# !/usr/bin/env python3
# coding=utf-8  
__author__ = 'retroxz'

import os
import nonebot
from utils.plugin_data import PLUGINS_DATA_DIR
from utils.config import Config
from colorama import init as colorInit
from .logger import logger
from datetime import datetime

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
    plugins_index = 0
    for plugin in Config.get('plugins', []):
        if plugin.startswith('nonebot'):
            nonebot.load_plugin(plugin)
        else:
            nonebot.load_plugin(F"plugins.{plugin}")
        plugins_index = plugins_index + 1
    if plugins_index == 0:
        logger.warning(F"Bot未加载任何插件")
    else:
        logger.success(F"Bot已加载{plugins_index}个插件")


def print_copy_right():
    colorInit()
    COPYRIGHT = F"\033[0;37;1m" + f"""
  _    _ _                                  ____        _   
 | |  | (_)                                |  _ \      | |  
 | |__| |_ _ __   __ _ _ __ ___   ___   ___| |_) | ___ | |_ 
 |  __  | | '_ \ / _` | '_ ` _ \ / _ \ / _ \  _ < / _ \| __|
 | |  | | | | | | (_| | | | | | | (_) |  __/ |_) | (_) | |_ 
 |_|  |_|_|_| |_|\__,_|_| |_| |_|\___/ \___|____/ \___/ \__|   
 
Copyright © 2019-{datetime.now().strftime('%Y')} HinamoeOfficial,All Rights Reserved
Project: https://github.com/retroxz/HinamoeBot
BOT数据目录: {BOT_PATH}                                                
""" + "\033[0m"
    print(COPYRIGHT)
