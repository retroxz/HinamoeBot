const schedule = require('node-schedule');
const GreetingModel = require('./model/Greeting')
const {Message} = require('mirai-ts')
exports.sendLastSleepTask = function (ctx) {
    const  scheduleCronStyle = () => {
        //每分钟的第30秒定时执行一次:
        schedule.scheduleJob('0 58 5 * * ? ', async () => {
            // 获取到列表
            let list = await GreetingModel.queryLastSleep()
            list.forEach(item => {
                let message = `👑是昨天的熬夜冠军！！！\n他昨天是${item.create_time.getHours()}:${item.create_time.getMinutes()}:${item.create_time.getSeconds()}睡的！！\n让我们恭喜他！`
                ctx.mirai.api.sendGroupMessage([Message.At(item.sender_id),Message.Plain(message)],item.group_id)
            })
        });
    }
    scheduleCronStyle()
}
