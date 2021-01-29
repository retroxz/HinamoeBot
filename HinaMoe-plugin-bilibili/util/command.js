const mt = require('mirai-ts')

// 指令实现
const biliSpace = require('../api/space')
const biliSearch = require('../api/search')
// 指令map
const commandsMap = new Map()

/**
 * 查询用户信息
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
    // 回复消息
    message.reply([mt.Message.Plain(replyMessage)])
  }
}

// 注册指令
commandsMap.set('用户信息', exports.searchUidInfo)

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
