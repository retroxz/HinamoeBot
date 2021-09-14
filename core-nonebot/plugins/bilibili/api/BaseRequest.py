#!/usr/bin/env python
# -*-coding:utf-8 -*-


import httpx
from httpx import ConnectTimeout, ReadTimeout
from utils import logger
from ..info import Error
from ..exception import *


async def request(method: str, url: str, **kw):
    """
    请求函数
    :param method: 请求方式
    :param url: 请求地址
    :param kw: 额外参数
    :return:
    """

    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(method, url, **kw)
            response_json = response.json()
            if response_json['code'] != 0:
                raise BiliRequestError(url, response_json['message'])
        except ConnectTimeout:
            logger.error(F"{Error.BILI_REQUEST_TIME_OUT}")
            raise
        except ReadTimeout:
            logger.error(F"{Error.BILI_READ_TIME_OUT}")
            raise
        except PluginsBaseException as e:
            logger.error(e.__str__())
            raise
        return response_json
