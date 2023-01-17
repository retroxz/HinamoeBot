from nonebot import on_command
from asyncio.exceptions import TimeoutError
from nonebot.typing import T_State



bt = on_command("bt")


@bt.handle()
async def _():
    pass


@bt.got("keyword", prompt="请输入要查询的内容！")
async def _():
    pass
