#!/usr/bin/env python
# -*-coding:utf-8 -*-


import httpx
from httpx import ConnectTimeout, ReadTimeout
from utils import logger
from ..info import Error


class BaseRequest:
    async def request(self, method: str, url: str, **kw):
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
            except ConnectTimeout:
                logger.error(F"{Error.BILI_REQUEST_TIME_OUT}")
                raise
            except ReadTimeout:
                logger.error(F"{Error.BILI_READ_TIME_OUT}")
                raise
            except:
                logger.error(F"{Error.BILI_UNKNOWN_ERROR}")
            print(response.text)
            return response_json

