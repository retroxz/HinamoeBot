# !/usr/bin/env python3
# coding=utf-8

"""
Space Service Class
"""
from typing import Optional

from .BaseRequest import BaseRequest
from utils import is_integer
from ..exception import BiliUserNotFoundException


class Space(BaseRequest):
    async def uid_info(self, uid):
        """
        获取bilibili用户资料卡
        :param uid: 用户uid或者昵称
        :return: 用户资料卡json
        """
        if not uid.isdigit():
            url = F"http://api.bilibili.com/x/web-interface/search/type?keyword={uid}&search_type=bili_user"
            response = await self.request('GET', url)
            if response['data']['numResults'] == 0:
                raise BiliUserNotFoundException(uid)
            uid = response.get('data').get('result')[0]['mid']
        response = await self.request('GET', F"http://api.bilibili.com/x/space/acc/info?mid={uid}")
        if not response.get('data'):
            raise BiliUserNotFoundException(uid)
        return response.get('data')
