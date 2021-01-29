const mt = require('mirai-ts')
const _util = require('util')
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
  let userInfo = {}
  let replyMessage = ''
  let uid = message.plain.split('订阅直播')[1]
  if (!uid) return
  if (isNaN(parseInt(uid))) {
    // 输入的是昵称 获取uid
    const searchRes = await biliSearch.searchUser(uid)
    uid = searchRes.data.result[0].mid
  }
  // 搜索用户信息
  userInfo.uid = uid
  const infoRes = await biliSpace.spaceInfo(userInfo.uid)
  // 保存昵称和直播间号
  userInfo.roomId = infoRes.data.live_room.roomid
  userInfo.nick = infoRes.data.name
  console.log(JSON.stringify(userInfo))

  // 生成参数
  const currentDate = new Date()
  if(message.type === MESSAGE_SCOPE.GROUP_MESSAGE.TYPE){
    // 群订阅
    userInfo.qid = message.sender.group.id
    userInfo.qnick = message.sender.group.name
    userInfo.operatorNick = message.sender.memberName
  }else if(message.type === MESSAGE_SCOPE.FRIEND_MESSAGE.TYPE){
    // 好友订阅
    userInfo.qid = message.sender.id
    userInfo.qnick = message.sender.nickname
    userInfo.operatorNick = message.sender.nickname
  }
  userInfo.type = SUBSCRIBE_SCOPE.LIVE
  userInfo.qtype = MESSAGE_SCOPE.GROUP_MESSAGE.ID
  userInfo.operatorId = message.sender.id
  userInfo.createTime = `${currentDate.getFullYear()}-${currentDate.getMonth() + 1}-${currentDate.getDate()} ${currentDate.getHours()}:${currentDate.getMinutes()}:${currentDate.getSeconds()}`

  console.log(JSON.stringify(userInfo))

  // 写入数据库
  let status = '失败'
  const res = await subscribesModel.add(userInfo)
  if(res.affectedRows === 1){
    status = '成功'
  }
  replyMessage = `[${userInfo.qnick}](${userInfo.qid})订阅[${userInfo.nick}]直播${status}！\n直播间：https://live.bilibili.com/${userInfo.roomId}`
  // 发送返回信息
  message.reply(replyMessage)
}


// 注册指令
commandsMap.set('用户信息', exports.searchUidInfo)
commandsMap.set('订阅直播', exports.addLiveSubscribe)

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
