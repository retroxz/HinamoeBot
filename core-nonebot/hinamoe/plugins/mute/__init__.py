import nonebot
from nonebot import on_command
from nonebot.plugin import on_notice
from nonebot.adapters.cqhttp.event import GroupBanNoticeEvent,GroupMessageEvent
from nonebot.rule import Rule
from nonebot.adapters import Bot, Event
from nonebot.typing import T_State


# 导入全局配置
global_config = nonebot.get_driver().config


def is_at():
    """
    验证是否是艾特消息
    :return:
    Bool 验证结果
    """

    async def _is_at(bot: Bot, event: Event, state: T_State) -> bool:
        try:
            if event.get_message()[1].type == 'at':
                return True
            else:
                return False
        except:
            pass

    return Rule(_is_at)


def is_group_mute_event():
    """
    验证是否为群禁言时间
    :return:
    Bool 验证结果
    """

    async def _is_group_mute_event(bot: Bot,event: Event,state: T_State) -> bool:
        # Todo 此处的 [event.duration > 0] 是因为Bot在为某成员解除禁言后 依然会触发一个sub_type为ban的事件 这里追加对禁言时间的验证
        if isinstance(event, GroupBanNoticeEvent) and event.sub_type == 'ban' and event.duration > 0:

            return True
        else:
            return False
    return Rule(_is_group_mute_event)


# 禁言
mute = on_command('mute', rule=is_at())
@mute.handle()
async def mute_handle(bot: Bot, event: GroupMessageEvent, state):
    await bot.call_api('set_group_ban', group_id=event.group_id, user_id=event.get_message()[0].data['qq'], duration=600)


# 解除禁言
unmute = on_command('unmute',rule=is_at())
@unmute.handle()
async def unmute_handle(bot: Bot, event: GroupMessageEvent, state: T_State):
    await bot.call_api('set_group_ban', group_id=event.group_id, user_id=event.get_message()[0].data['qq'], duration=0)


# 监听群组禁言
listen_group_mute = on_notice(rule=is_group_mute_event())
# @listen_group_mute.handle()
# async def demo_handle(bot: Bot, event: GroupBanNoticeEvent, state):
#     await bot.call_api('set_group_ban', group_id=event.group_id, user_id=event.user_id, duration=0)
#     await bot.call_api("send_group_msg",
#                            group_id=event.group_id,
#                            message=F"{MessageSegment.at(user_id=event.operator_id)}不要随便做坏事哦")



