#!/usr/bin/env python
# -*-coding:utf-8 -*-


import httpx
from utils import logger
from ..exception import *
from plugins.bilibili.utils.cache_bot import cache


async def request(method: str, url: str, origin=False, **kw):
    """
    请求函数
    :param origin: 返回原始response
    :param method: 请求方式
    :param url: 请求地址
    :param kw: 额外参数
    :return:
    """

    async with httpx.AsyncClient() as client:
        e = Exception()
        origin_response = await client.request(method, url, **kw)
        response = origin_response.json()
        if response.get('code') != 0:
            e = BiliRequestError(url, response, response)
            logger.error(e.__str__())
            raise e
        # 风控检测
        if response.get('code') == -412:
            e = BiliRefuseError(url, response, response)
            logger.error(e.__str__())
            raise e

        # except ConnectTimeout:
        #     logger.error(F"{Error.BILI_REQUEST_TIME_OUT}")
        #     raise
        # except ReadTimeout:
        #     logger.error(F"{Error.BILI_READ_TIME_OUT}")
        #     raise
        # except PluginsBaseException as e:
        #     logger.error(e.__str__())
        #     raise
        return origin_response if origin else response.get('data')
