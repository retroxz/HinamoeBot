import Bot from "el-bot";
import utils from "el-bot";
import { MessageType,check,Message } from "mirai-ts";

export default function (ctx: Bot){
    ctx.mirai.on('GroupMessage',message => {
        if(check.is(message.plain,['早','早安','早啊','早呀','早上好'])){
            message.reply(goodMorning().toDateString())
        }
    })
}

/**
 * 当说早安的时候
 */

function goodMorning(){
    let currentDate = new Date()
    // 当前小时小于6 归到前一天计算
    if(new Date().getHours() < 6){
        currentDate.setDate(currentDate.getDate() - 1)
    }
    return currentDate
}
