const help = new Map()
const {Message} = require('mirai-ts')

exports.match = function(message) {
    const plain = message.plain
    if (!plain) return 
    for (let key of help.keys()) {
        if (plain.indexOf(key) === 0) {
            help.get(key)(message)
        }
    }
}

exports.hinamoeHelp = function (message) {
    let text = '======== 雏萌帮助 ========\n 发送以下内容获取详细帮助\n'
    for (let key of help.keys()) {
        if（key === '雏萌帮助') continue
        else{
            text += `${key}\n`
        }
    }
    message.reply(text)
}
exports.danmakuHelp = function (message){
    let text = `弹幕库功能
    1. 【弹幕排行】每日弹幕排行 后面跟两位数日期可以查询指定日期排行
    例如: 弹幕排行03-05
    2.【弹幕语录XXX】随机显示XXX十条弹幕 可以填入昵称或UID
    注意: 每个群弹幕库不同 例如薯条相关群就是薯条弹幕库`

    message.reply(text)
}

exports.hhshHelp = function (message){
    let text = `好好说话功能
    格式: 好好说话+英文缩写`
    message.reply(text)
}

exports.greetingHelp = function (message){
    let text = `早晚安问候功能
    1. 群聊内发送诸如早安晚安之类的问候词语会收到bot回复
    2. 每个群分别排名 每天早安晚安限定一次
    3. ✨ 本功能尚在测试中 bug提交或功能建议直接私聊bot ✨`
    message.reply(text)
}

exports.fortuneHelp = function (message){
    let text = `求签功能
    格式: /求签+任意内容`
    message.reply(text)
}

exports.buttonHelp = function (message){
    const text = `按钮功能
    1. 来句啥: 将随机发送一个按钮
    2. 来句+按钮名字
    3. 按钮列表如下`
    const url = 'https://z3.ax1x.com/2021/03/23/67wgyt.png'
    message.reply([
        Message.Plain(text),
        Message.Image('',url)
    ])
}

exports.thankYou = function (message){
    let text = `======== 鸣谢 ========\n项目经理：疯狂的小智retro\n系统分析员：疯狂的小智retro\n结构工程师：疯狂的小智retro\n软件工程师：疯狂的小智retro\n硬件工程师：疯狂的小智retro\n软件测试工程师：疯狂的小智retro\n质量工程师：疯狂的小智retro\n其他人员：疯狂的小智retro\n`
    message.reply(text)
}

help.set("雏萌帮助",exports.hinamoeHelp)
help.set("问候帮助",exports.greetingHelp)
help.set("弹幕库帮助",exports.danmakuHelp)
help.set("好好说话帮助",exports.hhshHelp)
help.set("求签帮助",exports.fortuneHelp)
help.set("按钮帮助",exports.buttonHelp)
help.set("谢谢雏萌",exports.thankYou)
