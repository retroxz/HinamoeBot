from datetime import datetime
from hashlib import md5

from nonebot import on_startswith
from nonebot.adapters import Bot, Event
from nonebot.typing import T_State

ex = ['大吉', '吉', '半吉', '小吉', '末吉', '凶', '大凶', '小凶', '吉', '末小凶']
week = ['一', '二', '三', '四', '五', '六', '日']


def Date():
    dt = datetime.now()
    dateList = dt.timetuple()
    dateText = "{}年{}月{}日 星期{}".format(dateList[0], dateList[1], dateList[2], week[dateList[6]])
    return dateText


def md5Str(text: str):
    md = md5(text.encode("UTF-8")).hexdigest()
    md5Int = ...
    for i in md:
        if i.isdigit():
            md5Int = i
            break
    return md5Int


def _fortune(word):
    md5Int = md5Str(word)
    result = "【{}】".format(ex[int(md5Int)])
    return result


fortune = on_startswith("求签", priority=5)


@fortune.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    text = (str(event.get_message()).replace(" ", "")).split("求签")[-1]
    if text:
        state["fortune_word"] = text


@fortune.got("fortune_word", prompt="空的你是要求什么嘛！")
async def handle_fortune_word(bot: Bot, event: Event, state: T_State):
    text = state["fortune_word"]
    msg = "{}\n{}所求内容【{}】\n{}".format(Date(), event.sender.card, text, _fortune(text))
    await fortune.send(msg)
