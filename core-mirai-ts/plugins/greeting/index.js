const {default: Bot} = require('el-bot')
const { check,Message } = require('mirai-ts')
const GreetingModel = require('./model/Greeting')
const weekZh = ['日', '一', '二', '三', '四', '五', '六']


module.exports = async function (ctx){
    ctx.mirai.on('GroupMessage',message => {
        if(check.is(message.plain,['早','早安','早啊','早呀','早上好','早上花'])){
            goodMorning(message)
        }else if(check.is(message.plain,['晚','晚安','睡了','晚安了','晚上好','晚上花'])){
            goodNight(message)
        }
    })

}

/**
 * 当说早安的时候
 */

async function goodMorning(message) {
    let currentDate = new Date()
    let greetingStation = ''
    let currentDateStr = `${currentDate.getFullYear()}-${currentDate.getMonth() + 1}-${currentDate.getDate()} ${currentDate.getHours()}:${currentDate.getMinutes()}:${currentDate.getSeconds()}`
    // 查找上次记录
    let lastLog = await GreetingModel.queryLastGreetingLog({groupId: message.sender.group.id,senderId: message.sender.id,type: 2})
    if(lastLog.length > 0){
        let greetingTime = ((currentDate.getTime() / 1000) - (new Date(lastLog[0]['create_time']).getTime() / 1000))
        console.log(lastLog)
        if( greetingTime < 10800){
            greetingStation = `\n你才睡了${parseInt(greetingTime / 3600)}小时${parseInt((greetingTime % 3600) / 60)}分钟 再睡一会吧`
        }else if(greetingTime > 43200){
            greetingStation = `\n你竟然睡了${parseInt(greetingTime / 3600)}小时${parseInt((greetingTime % 3600) / 60)}分钟 虚拟树袋熊石锤了`
        }else{
            greetingStation = `\n你一共睡了${parseInt(greetingTime / 3600)}小时${parseInt((greetingTime % 3600) / 60)}分钟`
        }
    }
    let currentRank = await GreetingModel.addGreetingLog({
        groupId: message.sender.group.id,
        groupName: message.sender.group.name,
        senderId: message.sender.id,
        senderName: message.sender.memberName,
        type: 1,
        morning_time: currentDateStr,
        create_time: currentDateStr
    })
    if(currentRank === -1) return
    console.log(`${message.sender.memberName}`)
    console.log(currentRank)
    message.reply([Message.At(message.sender.id),Message.Plain(`现在是: ${currentDate.getFullYear()}年${currentDate.getMonth() + 1}月${currentDate.getDate()}日 星期${weekZh[currentDate.getDay()]}\n早上好 你是群里第【${currentRank}】位起床的哦${greetingStation}`)])
}

/**
 * 当说晚安的时候
 */

async function goodNight(message) {
    let currentDate = new Date()
    let currentDateStr = `${currentDate.getFullYear()}-${currentDate.getMonth() + 1}-${currentDate.getDate()} ${currentDate.getHours()}:${currentDate.getMinutes()}:${currentDate.getSeconds()}`
    let currentRank = await GreetingModel.addGreetingLog({
        groupId: message.sender.group.id,
        groupName: message.sender.group.name,
        senderId: message.sender.id,
        senderName: message.sender.memberName,
        type: 2,
        morning_time: currentDateStr,
        create_time: currentDateStr
    })
    if(currentRank === -1) return
    console.log(`${message.sender.memberName}`)
    console.log(currentRank)
    message.reply([Message.At(message.sender.id),Message.Plain(`现在是: ${currentDate.getFullYear()}年${currentDate.getMonth() + 1}月${currentDate.getDate()}日 星期${weekZh[currentDate.getDay()]}\n晚安啦 你是群里第【${currentRank}】位睡觉的哦`)])
}
