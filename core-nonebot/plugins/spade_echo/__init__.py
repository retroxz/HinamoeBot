import os
import nonebot
import random
from datetime import datetime
from nonebot import get_driver, on_startswith
import dateutil.parser
from dateutil.relativedelta import relativedelta
from nonebot.plugin import require
from nonebot.adapters import Bot, Event
from nonebot.typing import T_State
from nonebot.adapters.cqhttp.message import MessageSegment, Message


scheduler = require('nonebot_plugin_apscheduler').scheduler
driver = get_driver()
# 时间区间
station = {
    'evening': (19, 28),
    'morning': (5, 10),
    'noon': (11, 13),
    'afternoon': (14, 18)
}


# 随机出发动态的时间
@driver.on_startup
async def do_something():
    print(F'{__package__}插件已加载')
    scheduler.add_job(set_push_dynamic_task, 'cron', day_of_week='0-6', hour='0', minute='01')


# 发送动态
async def push_dynamic(dynamic_type):
    bot = list(nonebot.get_bots().values())[0]
    await bot.call_api("send_group_msg", group_id=0, message=F"{dynamic_type}")


# 生成发送动态定时任务
def set_push_dynamic_task():
    # 发动态的时间
    push_dynamic_hours = {
        # 早上
        'morning': dateutil.parser.parse(datetime.now().strftime(
            F"%Y-%m-%d {random.randint(station['morning'][0], station['morning'][1])}:{random.randint(0, 59)}:{random.randint(0, 59)}")),
        # 中午
        'noon': dateutil.parser.parse(datetime.now().strftime(
            F"%Y-%m-%d {random.randint(station['noon'][0], station['noon'][1])}:{random.randint(0, 59)}:{random.randint(0, 59)}")),
        # 下午
        'afternoon': dateutil.parser.parse(datetime.now().strftime(
            F"%Y-%m-%d {random.randint(station['afternoon'][0], station['afternoon'][1])}:{random.randint(0, 59)}:{random.randint(0, 59)}"))
    }
    # 夜间
    evening_hour = random.randint(station['evening'][0], station['evening'][1])
    if evening_hour >= 24:
        evening_hour -= 24
        current_date = datetime.now() + relativedelta(days=1)
        push_dynamic_hours['evening'] = dateutil.parser.parse(current_date.strftime(
            F"%Y-%m-%d {evening_hour}:{random.randint(0, 60)}:{random.randint(0, 60)}"))
    else:
        push_dynamic_hours['evening'] = dateutil.parser.parse(datetime.now().strftime(
            F"%Y-%m-%d {evening_hour}:{random.randint(0, 60)}:{random.randint(0, 60)}"))

    # 绑定定时任务
    scheduler.add_job(push_dynamic, 'date', run_date=push_dynamic_hours['morning'], args=['morning'])
    scheduler.add_job(push_dynamic, 'date', run_date=push_dynamic_hours['noon'], args=['noon'])
    scheduler.add_job(push_dynamic, 'date', run_date=push_dynamic_hours['afternoon'], args=['afternoon'])
    scheduler.add_job(push_dynamic, 'date', run_date=push_dynamic_hours['evening'], args=['evening'])


# 注册求签事件响应器
peach = on_startswith("桃宝", priority=5)  # 优先级为5


@peach.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    await peach.send(MessageSegment.image
        (
        ''))
    print(os.getcwd())
