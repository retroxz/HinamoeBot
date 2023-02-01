from nonebot import on_command
from asyncio.exceptions import TimeoutError

from nonebot.adapters.onebot.v11 import PrivateMessageEvent, Message, Bot, Event
from nonebot.internal.params import ArgStr
from nonebot.params import CommandArg
from nonebot.typing import T_State
from utils import is_integer
from .source import get_bt_info, get_download_link

bt = on_command("bt", priority=5, block=True)


@bt.handle()
async def _(state: T_State, arg: Message = CommandArg()):
    msg = arg.extract_plain_text().strip().split()
    if msg:
        keyword = None
        page = 1
        if n := len(msg):
            keyword = msg[0]
        if n > 1 and is_integer(msg[1]) and int(msg[1]) > 0:
            page = int(msg[1])
        state["keyword"] = keyword
        state["page"] = page
    else:
        state["page"] = 1


@bt.got("keyword", prompt="请输入要查询的内容！")
async def _aaa(
        bot: Bot, event: Event, state: T_State
):
    keyword = state['keyword']
    page = state['page']
    send_flag = False
    # try:
    async for title, type_, create_time, file_size, link in get_bt_info(
            keyword, page
    ):
        await bt.send(
            f"标题：{title}\n"
            f"类型：{type_}\n"
            f"创建时间：{create_time}\n"
            f"文件大小：{file_size}\n"
            f"种子：{link}"
        )
        send_flag = True


# except TimeoutError:
#     await bt.finish(f"搜索 {keyword} 超时...")
# except Exception as e:
#     await bt.finish(f"bt 其他未知错误..")
    if not send_flag:
        await bt.send(f"{keyword} 未搜索到...")
