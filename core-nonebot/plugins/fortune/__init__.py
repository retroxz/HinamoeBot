from datetime import datetime
from hashlib import md5

from nonebot import on_command
from nonebot.adapters import Bot, Event
from nonebot.typing import T_State

ex = ['大吉', '吉', '半吉', '小吉', '末吉', '大凶', '凶', '半凶', '小吉', '末凶']  # 求签结果选项
week = ['一', '二', '三', '四', '五', '六', '日']  # 将日期转换为汉字


# 获取格式化的日期字符串
def Date():
    dt = datetime.now()
    dateList = dt.timetuple()  # 包含各种时间信息的list
    dateText = "{}年{}月{}日 星期{}".format(dateList[0], dateList[1], dateList[2], week[dateList[6]])
    return dateText


# 获取由md5产生的单个随机数
def md5Str(text: str):
    md = md5(text.encode("UTF-8")).hexdigest()
    md5Int = ...
    for i in md:
        if i.isdigit():  # 判断是否为数字
            md5Int = i
            break
    return md5Int


# 由随机数得到求签结果
def _fortune(word):
    md5Int = md5Str(word)
    result = "【{}】".format(ex[int(md5Int)])
    return result


# 注册求签事件响应器
fortune = on_command("求签")  # 优先级为5


@fortune.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    origin_raw = str(event.get_message())
    raw = F"{origin_raw}{event.sender.user_id}{datetime.now().strftime('%Y%m%d')}"
    # 如果结果不为空，就存入T_State
    if origin_raw:
        state["origin_raw"] = origin_raw
        state["raw"] = raw


@fortune.got("origin_raw", prompt="告诉我求签的内容啊！")  # 求签内容为空时反馈
async def handle_fortune_word(bot: Bot, event: Event, state: T_State):
    origin_raw = state["origin_raw"]
    raw = state["raw"]
    msg = "{}\n{}所求内容【{}】\n{}".format(Date(), event.sender.card, origin_raw, _fortune(raw))
    await fortune.send(msg)
