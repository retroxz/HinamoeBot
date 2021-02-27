const {default: Bot} = require('el-bot')
const mt = require('mirai-ts')

module.exports = function (ctx){
  const mirai = ctx.mirai
  mirai.on('MemberMuteEvent',msg => {
    console.log(msg)
    // 获取到被禁言群号
    const groupId = msg.member.group.id
    // 获取被禁言的QQ
    const id = msg.member.id
    // 获取操作者
    const operatorId = msg.operator.id
    // 检查
    if(groupId === 1040339889 && (id === 853287614 || id === 405091647)){
      // 解除此人禁言
      mirai.api.unmute(groupId,id)
      // 发送一条警告
      mirai.api.sendGroupMessage([mt.Message.At(operatorId),mt.Message.Plain(' 不会让你得逞的mo~')],groupId)
    }
  })
}
