const {default: Bot} = require('el-bot')
const { Message } = require('mirai-ts')
const { check } = require("mirai-ts");
const biliLive = require('./api/live')
const schedule = require('node-schedule');
const Commands = require('./util/command')

// schedule.scheduleJob('*/5 * * * * ?', function() {
//   console.log('You will see this message every second');
// })
module.exports = async function (ctx) {
  const mirai = ctx.mirai
  // schedule.scheduleJob('*/5 * * * * ?', function () {
  //   console.log(ctx);
  // })
  // const obj = { live:['22603245','759938'] }
  // console.log(JSON.stringify(obj))
  // _redis.client().set('541613058',JSON.stringify(obj))
  // console.log()
  // const res = await mirai.api.uploadVoice('group','./plugins/custom/bilibili/voice/test.amr')
  // console.log(Message.Voice(res.voiceId))
  // const messageres = await mirai.api.sendGroupMessage([Message.Voice(res.voiceId)],1092438484)
  // console.log(messageres)
  // console.log(await biliLive.roomInfo(22603245))
  mirai.on('message',async msg => {
    Commands.match(msg)
  })
}



