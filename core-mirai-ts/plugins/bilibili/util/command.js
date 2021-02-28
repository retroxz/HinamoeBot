const mt = require('mirai-ts')

const biliSpace = require('../api/space')
const biliSearch = require('../api/search')
const subscribeService = require('../service/subscribes')
const SUBSCRIBE_SCOPE = require('../enum/SubscribeType')
// 指令map
const commandsMap = new Map()

/**
 * 查询用户信息
 * @command 用户信息<昵称 | uid>
 * @param message
 * @returns {Promise<void>}
 */
exports.searchUidInfo = async function (message) {
    // 截取用户消息文本 获取到指令参数
    let replyMessage = ''
    let uid = message.plain.split('用户信息')[1]
    if (!uid) return
    // 判断输入类型
    try {
        if (parseInt(uid) !== 'number') {
            // 搜索昵称获取uid
            const searchRes = await biliSearch.searchUser(uid)
            uid = searchRes.data.result[0].mid
        }
        // 发送请求 请求基本信息和粉丝数
        // 验证返回
        const baseInfo = await biliSpace.spaceInfo(uid)
        const cardInfo = await biliSpace.spaceInfoWithFans(uid)
        replyMessage = `用户UID: ${baseInfo.data.mid}\n昵称: ${baseInfo.data.name}\n签名: ${baseInfo.data.sign}\n等级: ${baseInfo.data.level}\n粉丝数：${cardInfo.data.card.fans}\n关注数：${cardInfo.data.card.friend}\n个人空间: https://space.bilibili.com/${uid}\n直播间: ${baseInfo.data.live_room.url}`
        const face = mt.Message.Image('', cardInfo.data.card.face)
        // 回复消息
        message.reply([mt.Message.Plain(replyMessage), face])
    } catch (e) {
        replyMessage = `找不到uid为: [${uid}]的用户信息`
        console.log(replyMessage)
        // 回复消息
        message.reply([mt.Message.Plain(replyMessage)])
    }
}

/**
 * 添加直播订阅
 * @param message
 * @returns {Promise<void>}
 */
exports.addLiveSubscribe = async function (message) {
    await subscribeService.addSubscribe({
        type: SUBSCRIBE_SCOPE.LIVE,
        command: '订阅直播',
        message
    })
}

/**
 * 添加动态订阅
 * @param message
 * @returns {Promise<void>}
 */
exports.addDynamicSubscribe = async function(message){
    await subscribeService.addSubscribe({
        type: SUBSCRIBE_SCOPE.DYNAMIC,
        command: '订阅动态',
        message
    })
}

/**
 * 添加视频订阅
 * @param message
 * @returns {Promise<void>}
 */
exports.addVideoSubscribe = async function(message){
    await subscribeService.addSubscribe({
        type: SUBSCRIBE_SCOPE.VIDEO,
        command: '订阅视频',
        message
    })
}

/**
 * 取消订阅直播
 * @param message
 * @returns {Promise<void>}
 */
exports.deleteLiveSubscribe = async function(message){
    await subscribeService.deleteSubscribe({
        type: SUBSCRIBE_SCOPE.LIVE,
        command: '取消订阅直播',
        message
    })
}

/**
 * 取消订阅动态
 * @param message
 * @returns {Promise<void>}
 */
exports.deleteDynamicSubscribe = async function(message){
    await subscribeService.deleteSubscribe({
        type: SUBSCRIBE_SCOPE.DYNAMIC,
        command: '取消订阅动态',
        message
    })
}

/**
 * 取消订阅视频
 * @param message
 * @returns {Promise<void>}
 */
exports.deleteVideoSubscribe = async function(message){
    await subscribeService.deleteSubscribe({
        type: SUBSCRIBE_SCOPE.VIDEO,
        command: '取消订阅视频',
        message
    })
}

/**
 * 直播订阅列表
 * @param message
 * @returns {Promise<void>}
 */
exports.showLiveSubscribeList = async function(message){
    await subscribeService.showSubscribeList({
        type: SUBSCRIBE_SCOPE.LIVE,
        message
    })
}

/**
 * 动态订阅列表
 * @param message
 * @returns {Promise<void>}
 */
exports.showDynamicSubscribeList = async function(message){
    await subscribeService.showSubscribeList({
        type: SUBSCRIBE_SCOPE.DYNAMIC,
        message
    })
}

/**
 * 视频订阅列表
 * @param message
 * @returns {Promise<void>}
 */
exports.showVideoSubscribeList = async function(message){
    await subscribeService.showSubscribeList({
        type: SUBSCRIBE_SCOPE.VIDEO,
        message
    })
}

// 注册指令
commandsMap.set('用户信息', exports.searchUidInfo)
commandsMap.set('订阅直播', exports.addLiveSubscribe)
commandsMap.set('订阅动态', exports.addDynamicSubscribe)
commandsMap.set('订阅视频', exports.addVideoSubscribe)
commandsMap.set('取消订阅直播', exports.deleteLiveSubscribe)
commandsMap.set('取消订阅动态', exports.deleteDynamicSubscribe)
commandsMap.set('取消订阅视频', exports.deleteVideoSubscribe)
commandsMap.set('直播订阅列表', exports.showLiveSubscribeList)
commandsMap.set('动态订阅列表', exports.showDynamicSubscribeList)
commandsMap.set('视频订阅列表', exports.showVideoSubscribeList)

/**
 * 指令匹配
 * @param message 消息对象
 */
exports.match = function (message) {
    // 获取消息文本
    const plain = message.plain
    if (!plain) return
    for (let key of commandsMap.keys()) {
        if (plain.indexOf(key) === 0) {
            commandsMap.get(key)(message)
        }
    }
}
