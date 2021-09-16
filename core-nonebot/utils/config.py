# !/usr/bin/env python3
# coding=utf-8  
__author__ = 'retroxz'

import sys

import yaml
import os
sys.path.append('../')

path = os.path.abspath(os.path.join('./', 'config.yml'))
config = yaml.load(open(path, 'r', encoding='utf-8').read(), Loader=yaml.FullLoader)


def configs(cls):
    Dict = config
    for name, value in Dict.items():
        setattr(cls, name, value)
    return cls

@configs
class Config(object):
    pass


