const mt = require('mirai-ts')
const Util = require('./util')
const biliSpace = require('../api/space')
const biliSearch = require('../api/search')
const MESSAGE_SCOPE = require('../scope/MessageEvent')
const SUBSCRIBE_SCOPE = require('../scope/SubscribeType')
const subscribesModel = require('../model/Subscribes')
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
 */
exports.addLiveSubscribe = async function (message) {
    // 截取用户消息文本 获取到指令参数
    // 用户信息对象
    try {
        let userInfo = {}
        let replyMessage = ''
        let uid = message.plain.split('订阅直播')[1]
        if (!uid) return
        if (isNaN(parseInt(uid))) {
            // 输入的是昵称 获取uid
            const searchRes = await biliSearch.searchUser(uid)
            if (!searchRes.data.result)
                throw new Error(`找不到uid为: [${uid}]的用户信息`)
            uid = searchRes.data.result[0].mid
        }
        // 查询该条信息是否订阅过
        const existRes = await subscribesModel.querySubscribeExist({
            type: SUBSCRIBE_SCOPE.LIVE,
            groupId: message.sender.group.id,
            uid
        })
        if (existRes[0])
            throw new Error(`[${message.sender.group.name}](${existRes[0].qid})已经订阅过${existRes[0].nick_name}的直播`)
        // 搜索用户信息
        userInfo.uid = uid
        const infoRes = await biliSpace.spaceInfo(userInfo.uid)
        // 保存昵称和直播间号
        userInfo.roomId = infoRes.data.live_room.roomid
        userInfo.nick = infoRes.data.name
        // 生成参数
        const currentDate = new Date()
        if (message.type === MESSAGE_SCOPE.GROUP_MESSAGE.TYPE) {
            // 群订阅
            userInfo.qid = message.sender.group.id
            userInfo.qnick = message.sender.group.name
            userInfo.operatorNick = message.sender.memberName
        }
        userInfo.type = SUBSCRIBE_SCOPE.LIVE
        userInfo.qtype = MESSAGE_SCOPE.GROUP_MESSAGE.ID
        userInfo.operatorId = message.sender.id
        userInfo.createTime = Util.getCurrentDateString()
        // 写入数据库
        let status = '失败'
        const res = await subscribesModel.add(userInfo)
        if (res.affectedRows === 1) {
            status = '成功'
        }
        replyMessage = `[${userInfo.qnick}](${userInfo.qid})订阅[${userInfo.nick}]直播${status}！\n直播间：https://live.bilibili.com/${userInfo.roomId}`
        // 发送返回信息
        message.reply(replyMessage)
    } catch (e) {
        message.reply(e.message)
    }
}

/**
 * 删除直播订阅
 * @param message
 * @returns {Promise<void>}
 */
exports.deleteLiveSubscribe = async function deleteLiveSubscribe(message) {
    try {
        let replyMessage = ''
        let searchRes = {}
        let uid = message.plain.split('取消订阅直播')[1]
        if (!uid) return
        if (isNaN(parseInt(uid))) {
            // 输入的是昵称 获取uid
            searchRes = await biliSearch.searchUser(uid)
            if (!searchRes.data.result) {
                throw new Error(`找不到uid为: [${uid}]的用户信息`)
            }
            uid = searchRes.data.result[0].mid
        }
        // 查询该条信息是否订阅过
        const existRes = await subscribesModel.querySubscribeExist({
            type: SUBSCRIBE_SCOPE.LIVE,
            groupId: message.sender.group.id,
            uid
        })
        if (!existRes[0])
            throw new Error(`[${message.sender.group.name}](${message.sender.group.id})没有订阅过该直播`)
        // 删除订阅
        const deleteRes = await subscribesModel.deleteSubscribeExist({
            type: SUBSCRIBE_SCOPE.LIVE,
            groupId: message.sender.group.id,
            uid
        })
        replyMessage = `群[${message.sender.group.name}]取消订阅直播[${existRes[0].nick_name}]${deleteRes.affectedRows ? '成功' : '失败'}!`
        message.reply(replyMessage)
    } catch (e) {
        message.reply(e.message)
    }

}

/**
 * 直播订阅列表
 * @param message
 * @returns {Promise<void>}
 */
exports.showLiveSubscribeList = async function showLiveSubscribeList(message) {
    try{
        let replyMessage = `群[${message.sender.group.name}]直播订阅列表:\n`
        if (message.plain !== '直播订阅列表')
            return
        const list = await subscribesModel.querySubscribeExist({filed: 'nick_name,uid', type: SUBSCRIBE_SCOPE.LIVE, groupId: message.sender.group.id, uid: '%'})
        if(list.length === 0){
            throw new Error(`群[${message.sender.group.name}]没有订阅任何直播!`)
        }
        for (let index = 0,len = list.length;index < len;index++)
            replyMessage += `${index + 1}. ${list[index]['nick_name']}(${list[index]['uid']})\n`
        message.reply(replyMessage)
    }catch (e) {
        message.reply(e.message)
    }
}
// 注册指令
commandsMap.set('用户信息', exports.searchUidInfo)
commandsMap.set('订阅直播', exports.addLiveSubscribe)
commandsMap.set('取消订阅直播', exports.deleteLiveSubscribe)
commandsMap.set('直播订阅列表', exports.showLiveSubscribeList)

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
