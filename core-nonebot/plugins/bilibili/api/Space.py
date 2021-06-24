# !/usr/bin/env python3
# coding=utf-8

"""
Space Service Class
"""
from typing import Optional

from .BaseRequest import BaseRequest


class Space(BaseRequest):
    async def get_user_info(self, uid):
        """
        获取用户信息(带直播间号)
        :param uid: 用户id
        :return:
        """
        url = 'http://api.bilibili.com/x/space/acc/info'
        params = { 'mid': uid }
        return await self.request('GET', url, params=params)

    async def get_user_card_info(self, uid):
        """
        获取用户卡片信息(带粉丝数)
        :param uid: 用户id
        :return:
        """
        url = 'http://api.bilibili.com/x/web-interface/card'
        params = { 'mid': uid }
        return await self.request('GET', url, params=params)

    async def search_user(self, keyword):
        url = 'http://api.bilibili.com/x/web-interface/search/type'
        params = {
            'keyword': keyword,
            'search_type': 'bili_user'
        }
        return await self.request('GET', url, params=params)
