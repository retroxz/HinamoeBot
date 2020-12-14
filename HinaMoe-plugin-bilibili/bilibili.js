const {default: Bot} = require('el-bot')
const mt = require('mirai-ts')
const { Message } = require('mirai-ts')
const biliLive = require('./api/live')
const schedule = require('node-schedule');

schedule.scheduleJob('*/5 * * * * ?', function() {
  console.log('You will see this message every second');
})


module.exports = async function (ctx){
  // const mirai = ctx.mirai
  // const res = await mirai.api.uploadVoice('group','./plugins/custom/bilibili/voice/test.amr')
  // console.log(Message.Voice(res.voiceId))
  // const messageres = await mirai.api.sendGroupMessage([Message.Voice(res.voiceId)],1092438484)
  // console.log(messageres)
  console.log(await biliLive.roomInfo(22603245))


}
