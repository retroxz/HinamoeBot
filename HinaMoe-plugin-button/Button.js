const {default: Bot} = require('el-bot')
const mt = require('mirai-ts')
const fs = require('fs')
let filename = []

//获取按钮名称
function buttonName(path) {
  let readDir = fs.readdirSync(path)
  readDir.forEach(function (value) {
    let name = (value.split(".amr"))[0]
    filename.push(name)
  })
  return filename
}
filename = buttonName("E:\\GitHub\\el-bot-template-master\\voice")
//切割消息
function splitMessage(message) {
  //切割并取出按钮名
  let name = message.split('来个')[1]
  if (name === '') {
    throw new Error('空的你是要听什么嘛')
  }else if(!(filename.includes(name))){
    throw new Error('没有这个啦！！！')
  }
  return name
}


module.exports = function (ctx) {
  const mirai = ctx.mirai
  mirai.on('GroupMessage', async msg => {
    if (mt.check.includes(msg.plain, "来个")) {
      try {
        let name = splitMessage(msg.plain)
        let voice = await mirai.api.uploadVoice("group", "\\GitHub\\el-bot-template-master\\voice\\" + name + ".amr")
        await mirai.api.sendGroupMessage([mt.Message.Voice(voice.voiceId, voice.path)],
          msg.sender.group.id)
      } catch (e) {
        msg.reply(e.message)
      }
    }

  })
}
