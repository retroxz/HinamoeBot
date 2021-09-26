#!/usr/bin/env python
# -*-coding:utf-8 -*-


import httpx
from httpx import ConnectTimeout, ReadTimeout
from utils import logger
from ..info import Error
from ..exception import *


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
        try:
            origin_response = await client.request(method, url, **kw)
            response = origin_response.json()
            if response['code'] != 0:
                raise BiliRequestError(url, response, response)

            # 风控检测
            if response['code'] == -412:
                raise BiliRefuseError(url, response, response)

        except ConnectTimeout:
            logger.error(F"{Error.BILI_REQUEST_TIME_OUT}")
            raise
        except ReadTimeout:
            logger.error(F"{Error.BILI_READ_TIME_OUT}")
            raise
        except PluginsBaseException as e:
            logger.error(e.__str__())
            raise
        return origin_response if origin else response.get('data')
