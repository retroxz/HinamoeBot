#!/usr/bin/env python3
# coding=utf-8

"""
@File: logger.py
@Author: retroxz
@Email: zzxee666@gmail.com
@Date: 2021/04/23

logger 工具类
"""


import sys
from loguru import logger
from utils.utils import BOT_PATH

logger_format = (
    "<g>{time:MM-DD HH:mm:ss}</g> "
    "[<lvl>{level}</lvl>] "
    "<c><u>{name}</u></c> | "
    "{message}")

logger.remove()

logger.add(sys.stdout, colorize=True, format=logger_format)
logger.add(BOT_PATH + "/logs/{time: YYYY-MM}/{time: DD}.log", format=logger_format, rotation='00:00')
