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
    //判断早安时间
    if(currentDate.getHours() < 6 || currentDate.getHours() >= 12){
       message.reply([Message.At(message.sender.id),Message.Plain(`现在几点了还早安?`)])
       return
    }
    // 查找今天是否打过卡
    let flag = await GreetingModel.queryGreetingLog({groupId: message.sender.group.id,senderId: message.sender.id,type: 1})
    if(flag.length > 0) {
        message.reply([Message.At(message.sender.id),Message.Plain(`你已经早安过了`)])
        return
    }
    // 查找上次记录
    let lastLog = await GreetingModel.queryLastGreetingLog({groupId: message.sender.group.id,senderId: message.sender.id,type: 2})
    let greetingStation = getGreetingStation(currentDate, lastLog)
    //获取早安提示
    let morningTip = getMorningTip(currentDate.getHours())
    let currentDateStr = `${currentDate.getFullYear()}-${currentDate.getMonth() + 1}-${currentDate.getDate()} ${currentDate.getHours()}:${currentDate.getMinutes()}:${currentDate.getSeconds()}`
    let currentRank = await GreetingModel.addGreetingLog({
        groupId: message.sender.group.id,
        groupName: message.sender.group.name,
        senderId: message.sender.id,
        senderName: message.sender.memberName,
        type: 1,
        morning_time: currentDateStr,
        create_time: currentDateStr
    })
    if(currentRank === -1) {
        message.reply([Message.At(message.sender.id),Message.Plain(`你已经早安过了`)])
        return
    }
    console.log(`${message.sender.memberName}`)
    console.log(currentRank)
    message.reply([Message.At(message.sender.id),Message.Plain(`现在是: ${currentDate.getFullYear()}年${currentDate.getMonth() + 1}月${currentDate.getDate()}日 星期${weekZh[currentDate.getDay()]}\n 你是群里第【${currentRank}】位起床的哦${greetingStation} ${morningTip}`)])
}

/**
 * 当说晚安的时候
 */

async function goodNight(message) {
    let currentDate = new Date()
    //判断晚安时间
    if(currentDate.getHours() > 6 && currentDate.getHours() < 22){
       message.reply([Message.At(message.sender.id),Message.Plain(`现在几点了还晚安?`)])
       return
    }
    // 查找今天是否打过卡
    let flag = await GreetingModel.queryGreetingLog({groupId: message.sender.group.id,senderId: message.sender.id,type: 2})
    if(flag.length > 0) {
        message.reply([Message.At(message.sender.id),Message.Plain(`你已经晚安过了`)])
        return
    }
    //获取晚安提示
    let eveningTip = getEveningTip(currentDate.getHours())
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
    if(currentRank === -1) {
        message.reply([Message.At(message.sender.id),Message.Plain(`你已经晚安过了`)])
        return
    }
    console.log(`${message.sender.memberName}`)
    console.log(currentRank)
    message.reply([Message.At(message.sender.id),Message.Plain(`现在是: ${currentDate.getFullYear()}年${currentDate.getMonth() + 1}月${currentDate.getDate()}日 星期${weekZh[currentDate.getDay()]}\n 你是群里第【${currentRank}】位睡觉的哦 ${eveningTip}`)])
}

function getGreetingStation(currentDate, lastLog) {
    let greetingStation = ''
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
    return greetingStation
}

function getMorningTip(hours) {
    let morningTip = ''
    if(hours <= 9){
        morningTip = `起得真早`
    }else{
        morningTip = `太阳都晒屁股了`
    }
    return morningTip
}

function getEveningTip(hours) {
    let eveningTip = ''
    if(hours >= 2 && hours < 6){
        eveningTip = `再不睡觉就等着猝死吧`
    }else{
        eveningTip = `健康作息`
    }
    return eveningTip
}
