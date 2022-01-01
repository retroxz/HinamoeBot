# -*- coding: utf-8 -*-
# @Time    : 2021/12/30 11:03
# @Author  : retroxz
# @Email   : zzxee666@gmail.com
# @File    : dynamic.py

__author__ = "retroxz"

from ..model.subscribe import query_subscribe, update_last_dynamic_time
from ..utils import filter_subscribes
from ..api.dynamic import get_new_dynamic
import json
from utils.logger import logger
import time
from nonebot.adapters.cqhttp import MessageSegment
from utils import send_message
import inspect


async def get_new_dynamic_task():
    """
    获取新动态并推送任务
    :return:
    """
    raws = await query_subscribe()
    sub_data = filter_subscribes(raws)
    for uid in sub_data.keys():
        # 遍历订阅列表 获取动态信息
        dynamic_info = await get_new_dynamic(uid)
        # 遍历推送群列表
        for sub in sub_data[uid]:
            # 该群没有推送记录 把最新动态时间写入 这次不推送
            if not sub['last_dynamic_time']:
                last_dynamic_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                                  time.localtime(dynamic_info['cards'][0]['desc']['timestamp']))
                await update_last_dynamic_time(sub['id'], last_dynamic_time)
                continue

            # 有推送记录 检查是否有新动态
            new_dynamic = await filter_new_dynamic(sub, dynamic_info['cards'])
            if new_dynamic:
                # 推送动态
                await push_new_dynamic(sub, new_dynamic)
                # 更新动态时间
                last_dynamic_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                                  time.localtime(new_dynamic[0]['desc']['timestamp']))
                await update_last_dynamic_time(sub['id'], last_dynamic_time)


async def filter_new_dynamic(sub, dynamics):
    new_dynamics = []
    for dynamic in dynamics:
        # 1. 检查是否为可解析的动态类型
        """
            1 动态转发 [✓]
            4 原创动态 [✓]
            2 带图动态 [✓]
            8 视频发布 [✓]
            64 专栏发布
            2048 B站特殊活动分享

        """
        if dynamic['desc']['type'] not in [1, 4, 2, 8]:
            logger.warning(F"不可解析的动态类型{dynamic}")
            continue
        # 检查每条动态是否在数据库保存的最新动态之后
        last_dynamic_timestamp = int(sub['last_dynamic_time'].timestamp())
        if last_dynamic_timestamp < dynamic['desc']['timestamp']:
            new_dynamics.append(dynamic)
        else:
            break
    return new_dynamics


async def push_new_dynamic(sub, new_dynamics):
    for dynamic in new_dynamics:
        # 解析动态信息
        message = generate_dynamic_push_message(dynamic)
        print(message)
        # 发送消息
        await send_message(message, sub['qid'], sub['qtype'])


def generate_dynamic_push_message(dynamic):
    message = ""
    # 获取用户昵称
    uname = dynamic['desc']['user_profile']['info']['uname']
    # 获取动态类型
    dynamic_type = dynamic['desc']['type']
    # 解析动态正文
    card = json.loads(dynamic['card'])

    # 解析视频发布动态
    if dynamic_type == 8:
        message = F"""
        {uname}发布了新视频
        {card['title']}
        {MessageSegment.image(file=card['pic'])}
        传送门: {card['short_link_v2']}
        """

    # 解析转发动态
    if dynamic_type == 1:
        # 解析原动态
        origin_dynamic = json.loads(card['origin'])
        message = F"""
        {uname}转发了动态
        {card['item']['content']}
        传送门: https://t.bilibili.com/{dynamic['desc']['dynamic_id']}
        「原动态」
        """

        # 转发类型: 动态
        if 'user' in origin_dynamic.keys():
            message = message + F"{origin_dynamic['user']['name']}: {origin_dynamic['item']['description']}"
            # 添加图片
            pictures = origin_dynamic['item']['pictures']
            for pic in pictures:
                message = message + str(MessageSegment.image(file=pic['img_src']))

        # 转发类型: 视频
        if 'aid' in origin_dynamic.keys():
            message = message + F"{origin_dynamic['owner']['name']}的视频: {origin_dynamic['title']}"
            # 视频封面
            message = message + str(MessageSegment.image(file=origin_dynamic['pic']))

    # 解析原创动态
    if dynamic_type in [4, 2]:
        message = F"""
        {uname}发布了动态
        {card['item'].get('content') or card['item'].get('description')}
        传送门: https://t.bilibili.com/{dynamic['desc']['dynamic_id']}
        """
        if 'pictures' in card['item'].keys():
            for pic in card['item']['pictures']:
                message = message + str(MessageSegment.image(file=pic['img_src']))

    return inspect.cleandoc(message)
