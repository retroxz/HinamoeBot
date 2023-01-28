from nonebot import on_command
from asyncio.exceptions import TimeoutError




bt = on_command("bt")


@bt.handle()
async def _(state,  arg):
    msg = arg.extract_plain_text().strip().split()
    if msg:
        keyword = None
        page = 1
        if n := len(msg):
            keyword = msg[0]
        if n > 1 and is_number(msg[1]) and int(msg[1]) > 0:
            page = int(msg[1])
        state["keyword"] = keyword
        state["page"] = page
    else:
        state["page"] = 1


@bt.got("keyword", prompt="请输入要查询的内容！")
async def _():
    pass
