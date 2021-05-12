import nonebot
from nonebot import on_command
from nonebot.permission import SUPERUSER
from nonebot.plugin import on_notice
from nonebot.adapters.cqhttp.event import GroupBanNoticeEvent, GroupMessageEvent
from nonebot.rule import Rule, to_me
from nonebot.adapters import Bot, Event
from nonebot.typing import T_State
from nonebot.adapters.cqhttp.message import MessageSegment, Message
from utils import Plugin_Data, info
from utils.db import db_query
from .config import defend_member
import inspect

driver = nonebot.get_driver()
PLUGIN_NAME = __package__


@driver.on_startup
async def _():
    info(F"{__package__}已加载")


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

    async def _is_group_mute_event(bot: Bot, event: Event, state: T_State) -> bool:
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
    await bot.call_api('set_group_ban', group_id=event.group_id, user_id=event.get_message()[0].data['qq'],
                       duration=600)


# 解除禁言
unmute = on_command('unmute', rule=is_at())


@unmute.handle()
async def unmute_handle(bot: Bot, event: GroupMessageEvent, state: T_State):
    await bot.call_api('set_group_ban', group_id=event.group_id, user_id=event.get_message()[0].data['qq'], duration=0)


# 监听群组禁言
listen_group_mute = on_notice(rule=is_group_mute_event())


@listen_group_mute.handle()
async def listen_group_mute_handle(bot: Bot, event: GroupBanNoticeEvent, state):
    # 查询此人是否受保护
    result = await db_query(F"""SELECT sender_id, sender_name FROM bot.mute_defend 
                    WHERE group_id={event.group_id} AND sender_id={event.user_id}""")
    if len(result):
        await bot.call_api('set_group_ban', group_id=event.group_id, user_id=event.user_id, duration=0)
        await listen_group_mute.finish(Message(F"根据群员保护计划 为{MessageSegment.at(user_id=event.user_id)}解除禁言"))


# 添加保护计划
add_defend_member = on_command('add_defend', permission=SUPERUSER)


@add_defend_member.handle()
async def add_defend_member_handle(bot: Bot, event: GroupMessageEvent, state: T_State):
    # 获取群名片
    card_info = await bot.call_api('get_group_member_info',
                                   group_id=event.group_id,
                                   user_id=event.message[0].data['qq'])
    card = card_info['nickname'] if card_info['card'] == '' else card_info['card']
    if card_info['role'] != 'member':
        await add_defend_member.finish(F"{card}不能加入保护计划")
        return
    # 构建配置对象
    result = await db_query(F"""SELECT sender_id, sender_name FROM bot.mute_defend 
                       WHERE group_id={event.group_id} AND sender_id={event.user_id}""")
    if len(result):
        await add_defend_member.finish(F"{card}已经在保护计划中")
        return
    add_defend_sql = F"""
        INSERT INTO bot.mute_defend 
        (group_id, group_name, sender_id,sender_name,operator_id,operator_name)
        VALUES
	    ({event.group_id},'',{event.message[0].data['qq']},'{card}',{event.user_id},'{event.sender.card}');
    """
    print(add_defend_sql)
    await db_query(add_defend_sql)
    await add_defend_member.finish(F"{card}已加入保护计划")

# 移除保护计划
delete_defend_member = on_command('delete_defend', permission=SUPERUSER)


@delete_defend_member.handle()
async def delete_defend_member_handle(bot: Bot, event: GroupMessageEvent, state: T_State):
    # 获取群名片
    card_info = await bot.call_api('get_group_member_info',
                                   group_id=event.group_id,
                                   user_id=event.message[0].data['qq'])

    card = card_info['nickname'] if card_info['card'] == '' else card_info['card']
    pd = Plugin_Data(PLUGIN_NAME)
    d = defend_member(event.message[0].data['qq'], event.group_id, card)
    if pd.query(d):
        pd.delete(d)
        await delete_defend_member.finish(F"{card}已从保护计划中移除")
    else:
        await delete_defend_member.finish(F"{card}尚未在保护计划中")


# 保护计划列表
defend_member_list = on_command('defend_list')


@defend_member_list.handle()
async def defend_member_list_handle(bot: Bot, event: GroupMessageEvent, state: T_State):
    # print(nonebot.get_bots().values())
    # pd = Plugin_Data(PLUGIN_NAME)
    # defend_list = pd.db.table('defend_member').search(Query().group_id == str(event.group_id))
    #
    # message = F"""
    # 本群当前的保护名单:
    # """
    # index = 1
    # for item in defend_list:
    #     message += F"{index}. {item['card']}({item['qq']})\n"
    #     index += 1
    # if len(defend_list) == 0:
    #     message += "空"
    # await defend_member_list.finish(inspect.cleandoc(message))
    await db_query(sql="SELECT * FROM bot.bot_subscribes")
