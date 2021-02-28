/**
 * 订阅功能实现
 */
const biliSpace = require('../api/space')
const biliSearch = require('../api/search')
const subscribesModel = require('../model/Subscribes')
const MESSAGE_SCOPE = require('../enum/MessageEvent')
const Util = require('../util/util')


/**
 * 添加订阅
 * @param type
 * @param command
 * @param message
 */
exports.addSubscribe = async function addSubscribe({type, command, message}) {
    // 截取用户消息文本 获取到指令参数
    // 用户信息对象
    try {
        let userInfo = {}
        let replyMessage = ''
        let uid = message.plain.split(command)[1]
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
            type: type.ID,
            groupId: message.sender.group.id,
            uid
        })
        if (existRes[0])
            throw new Error(`[${message.sender.group.name}](${existRes[0].qid})已经订阅过${existRes[0].nick_name}的${type.VALUE}`)
        // 搜索用户信息
        userInfo.uid = uid
        const infoRes = await biliSpace.spaceInfo(userInfo.uid)
        // 保存昵称和直播间号
        userInfo.roomId = infoRes.data.live_room.roomid
        userInfo.nick = infoRes.data.name
        // 生成参数
        if (message.type === MESSAGE_SCOPE.GROUP_MESSAGE.TYPE) {
            // 群订阅
            userInfo.qid = message.sender.group.id
            userInfo.qnick = message.sender.group.name
            userInfo.operatorNick = message.sender.memberName
        }
        userInfo.type = type.ID
        userInfo.qtype = MESSAGE_SCOPE.GROUP_MESSAGE.ID
        userInfo.operatorId = message.sender.id
        userInfo.createTime = Util.getCurrentDateString()
        // 写入数据库
        const res = await subscribesModel.add(userInfo)
        replyMessage = `[${userInfo.qnick}](${userInfo.qid})订阅[${userInfo.nick}]${type.VALUE}${res.affectedRows === 1 ? '成功' : '失败'}！\n直播间：https://live.bilibili.com/${userInfo.roomId}`
        // 发送返回信息
        message.reply(replyMessage)
    } catch (e) {
        message.reply(e.message)
    }
}

/**
 * 删除订阅
 * @param type
 * @param command
 * @param message
 * @returns {Promise<void>}
 */
exports.deleteSubscribe = async function deleteSubscribe({type, command, message}) {
    try {
        let replyMessage = ''
        let searchRes = {}
        let uid = message.plain.split(command)[1]
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
            type: type.ID,
            groupId: message.sender.group.id,
            uid
        })
        if (!existRes[0])
            throw new Error(`[${message.sender.group.name}](${message.sender.group.id})没有订阅过该${type.VALUE}`)
        // 删除订阅
        const deleteRes = await subscribesModel.deleteSubscribeExist({
            type: type.ID,
            groupId: message.sender.group.id,
            uid
        })
        replyMessage = `群[${message.sender.group.name}]取消订阅${type.VALUE}[${existRes[0].nick_name}]${deleteRes.affectedRows ? '成功' : '失败'}!`
        message.reply(replyMessage)
    } catch (e) {
        message.reply(e.message)
    }

}

/**
 * 订阅列表
 * @param type
 * @param message
 * @returns {Promise<void>}
 */
exports.showSubscribeList = async function showSubscribeList({type,message}) {
    try {
        let replyMessage = `群[${message.sender.group.name}]${type.VALUE}订阅列表:\n`
        /*        if (message.plain !== '直播订阅列表')
                    return*/
        const list = await subscribesModel.querySubscribeExist({
            filed: 'nick_name,uid',
            type: type.ID,
            groupId: message.sender.group.id,
            uid: '%'
        })
        if (list.length === 0) {
            throw new Error(`群[${message.sender.group.name}]没有订阅任何${type.VALUE}!`)
        }
        for (let index = 0, len = list.length; index < len; index++)
            replyMessage += `${index + 1}. ${list[index]['nick_name']}(${list[index]['uid']})\n`
        message.reply(replyMessage)
    } catch (e) {
        message.reply(e.message)
    }
}
