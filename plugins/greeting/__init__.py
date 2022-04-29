# !/usr/bin/env python3
# coding=utf-8

from nonebot import on_keyword, on_startswith, on_regex
from nonebot.adapters import Bot, Event
from .greetings import Greeting
from .model import query_greeting_log, add_greeting_log
from nonebot.adapters.cqhttp import GroupMessageEvent
from datetime import datetime
from utils import get_group_info
import inspect

# morning_keyword = {'早安', '早啊', '早呀', '早上好', '早上花'}
morning_regex = '(^早$)|(^早安$)|(^早啊$)|(^早呀$)|(^早上好$)|(^早上花$)'
night_regex = '(^晚安$)|(^睡了$)|(^呼呼$)|(^呼呼喵$)'


# morning = on_keyword(morning_keyword)
morning = on_regex(morning_regex)
night = on_regex(night_regex)


@morning.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    # 查找打卡记录
    log = await query_greeting_log(event.group_id, event.user_id, 1)
    if not log:
        # 新增打卡记录
        group_info = await get_group_info(event.group_id, bot)
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        rank = await add_greeting_log(event.group_id, group_info['group_name'], event.user_id, event.sender.nickname, 1,
                                      current_date, current_date)
        message = F"""
        现在是{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        你是群里第【{rank}】个起床的人哦
        """
        await morning.finish(inspect.cleandoc(message))
    else:
        log = log[0]
        message = F"""
               你是群里第【{log['rank']}】个起床的人哦
               你的起床时间是: {log['create_time'].strftime('%H:%M:%S')}
               """
        await morning.finish(inspect.cleandoc(message))


@night.handle()
async def _(bot: Bot, event:GroupMessageEvent):
    # 查找打卡记录
    log = await query_greeting_log(event.group_id, event.user_id, 2)
    if not log:
        # 新增打卡记录
        group_info = await get_group_info(event.group_id, bot)
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        rank = await add_greeting_log(event.group_id, group_info['group_name'], event.user_id, event.sender.nickname, 2,
                                      current_date, current_date)
        message = F"""
           现在是{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
           你是群里第【{rank}】个睡觉的人哦
           """
        await morning.finish(inspect.cleandoc(message))
    else:
        message = F"""
                  你是群里第【{log['rank']}】个睡觉的人哦
                  你的起床时间是: {log['create_time'].strftime('%H:%M:%S')}
                  """
        await morning.finish(inspect.cleandoc(message))