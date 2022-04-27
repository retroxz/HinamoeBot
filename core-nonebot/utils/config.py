# !/usr/bin/env python3
# coding=utf-8  
__author__ = 'retroxz'

import sys
import yaml
import os

from .logger import logger
from munch import DefaultMunch

sys.path.append('../')


class Config:
    _Config = None

    @staticmethod
    def get(keys='', default=None):
        try:
            if Config._Config is None:
                Config.config_init()

            if keys == '':
                return Config._Config
            value = eval(F"Config._Config.{keys}")
            if value is None:
                return default
            return value
        except AttributeError:
            return default

    @staticmethod
    def config_init():
        # 读取配置文件
        path = os.path.abspath(os.path.join('./', 'config.yml'))
        if not os.path.exists(path):
            logger.error(F"读取配置失败 找不到文件{path}")
            sys.exit()
        config_dict = yaml.load(open(path, 'r', encoding='utf-8').read(), Loader=yaml.FullLoader)
        Config._Config = DefaultMunch.fromDict(config_dict)
        logger.success(F"读取配置成功 {path}")
