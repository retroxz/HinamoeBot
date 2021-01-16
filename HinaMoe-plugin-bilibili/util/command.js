// 指令实现
const biliSpace = require('../api/space')
// 指令map
const commandsMap = new Map()

exports.searchUidInfo = async function (message) {
  // Todo 加入用户头像和粉丝数的显示
  // 截取用户消息文本 获取到指令参数
  const uid = message.plain.split('uid信息')[1]
  // 发送请求
  if(!uid) return
  const res = await biliSpace.spaceInfo(uid)
  // 验证返回
  let replyMessage = res.code === 0?
    `用户UID: ${res.data.mid}\n昵称: ${res.data.name}\n签名: ${res.data.sign}\n等级: ${res.data.level}\n个人空间: https://space.bilibili.com/${uid}\n直播间: ${res.data.live_room.url}`:
    `找不到uid为: [${uid}]的用户信息`
  // 回复消息
  message.reply(replyMessage)
}

// 注册指令
commandsMap.set('uid信息',exports.searchUidInfo)

/**
 * 指令匹配
 * @param message 消息对象
 */
exports.match = function (message){
  // 获取消息文本
  const plain = message.plain
  if(!plain) return
  for (let key of commandsMap.keys()){
    if(plain.indexOf(key) === 0){
      commandsMap.get(key)(message)
    }
  }
}
