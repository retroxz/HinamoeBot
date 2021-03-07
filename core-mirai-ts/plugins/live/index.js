const {default: Bot} = require('el-bot')
const LiveApi = require('./live')
const { Message,} = require('mirai-ts')
let lastLiveTimeMap = {}
let mirai = {}
module.exports = async function (ctx) {
    mirai = ctx.mirai
    setInterval(listenLiveStatus,30000,ctx.el.bot.live)
}
function listenLiveStatus(config){
    config.forEach(async function (data){
        let res = await LiveApi.getLiveRoomInfoasync(data.live)
        const currentLiveTime = res.data.room_info.live_start_time
       if(res.data.room_info.live_status !== 0){
           if(currentLiveTime === lastLiveTimeMap[data.live]){
               console.log('已经推送过了')
           }else{
               lastLiveTimeMap[data.live] = currentLiveTime
               console.log(`推送: ${data.live}`)
               sendLiveMessage(data.group,res.data)
           }
       }
        console.log(lastLiveTimeMap)
    })
}
function sendLiveMessage(groupIds,data){
    let liveMsg = `${data.anchor_info.base_info.uname}开播啦!\n【${data.room_info.title}】\nhttps://live.bilibili.com/${data.room_info.room_id}`
    groupIds.forEach(function (groupId){
        mirai.api.sendGroupMessage([Message.AtAll(),Message.Plain(liveMsg)],groupId)
    })
}
