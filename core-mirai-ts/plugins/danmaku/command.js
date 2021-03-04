const commandsMap = new Map()
const Util = require('./utils')
const DanmakuModel = require('./model/Danmaku')

exports.danmakuRank = async function (message) {
    const dateRegex = '(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])'
    const queryDate = message.plain.split('弹幕排行')[1].replace(' ', '')
    let currentDate = new Date()
    // 两位日期正则
    try {
        if (queryDate) {
            // 输入了日期参数 验证参数
            if (queryDate.search(dateRegex) !== 0) {
                throw new Error('日期格式不对呀')
            }
            currentDate = new Date(`2021-${queryDate}`)
            if (!(currentDate instanceof Date && !isNaN(currentDate.getTime()))) {
                throw new Error('日期格式不对呀')
            }
        }
        const res = await DanmakuModel.danmakuRankByDate(currentDate)
        if (res.length === 0)
            throw new Error(`找不到${Util.getCurrentDateString(currentDate)}的弹幕记录！`)
        let replyMsg = `${Util.getCurrentDateString(currentDate)} 弹幕TOP10:\n`
        for (let i = 0, len = res.length; i < len; i++) {
            replyMsg += `${i + 1}: ${res[i]['昵称']}: ${res[i]['弹幕量']}条\n`
        }
        message.reply(replyMsg)
    } catch (e) {
        message.reply(e.message)
    }
}
commandsMap.set('弹幕排行', exports.danmakuRank)

exports.match = function (message) {
    const plain = message.plain
    if (!plain) return
    for (let key of commandsMap.keys()) {
        if (plain.indexOf(key) === 0) {
            commandsMap.get(key)(message)
        }
    }
}
