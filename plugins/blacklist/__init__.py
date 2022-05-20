from nonebot import on_command
from nonebot.permission import SUPERUSER
from nonebot import Bot
from nonebot.adapters.cqhttp import GroupMessageEvent, PrivateMessageEvent
from .model import BlacklistModel
from cacheout import Cache
from nonebot import get_driver
from utils.logger import logger
from nonebot.message import event_preprocessor

driver = get_driver()
add_black_user = on_command('add_black', permission=SUPERUSER)
# test = on_command('t', permission=SUPERUSER)
blacklist_cache = Cache()


@add_black_user.handle()
async def _(bot: Bot, event):
    print(event)
    message = event.get_message()
    if len(message) == 0 or message[0].type != 'at':
        await add_black_user.finish('命令后面at要拉黑的人!')
        return

    # 获取拉黑人QQ
    qid = message[0].data['qq']
    if qid in bot.config.superusers:
        await add_black_user.finish('不能拉黑超级管理员哦!')
        return

    # 查询是否存在
    result = await BlacklistModel.query_user(qid)
    if len(result) > 0:
        await add_black_user.finish('已存在的拉黑用户')
        return

    # 添加拉黑记录
    await BlacklistModel.add_black_user(qid)
    # 更新黑名单缓存
    blacklist_users = blacklist_cache.get('blacklist_users', default=[])
    blacklist_users.append(qid)
    blacklist_cache.set('blacklist_users', blacklist_users)

    await add_black_user.finish(F"已拉黑用户: {qid}")
    return


@driver.on_bot_connect
async def _(bot):
    result = await BlacklistModel.all()
    blacklist_users = []
    for data in result:
        blacklist_users.append(data['qid'])
    blacklist_cache.set('blacklist_users', blacklist_users)

    logger.success(F"加载{len(blacklist_users)}条黑名单记录")


@event_preprocessor
async def _(bot, event, state):
    if isinstance(event, GroupMessageEvent) or isinstance(event, PrivateMessageEvent):
        print(event)
        qid = event.get_user_id()
        b = blacklist_cache.get('blacklist_users', [])
        if int(qid) in blacklist_cache.get('blacklist_users', []):
            logger.info(F"{qid}的消息已被屏蔽")
            raise Exception(F"{qid}的消息已被屏蔽")
