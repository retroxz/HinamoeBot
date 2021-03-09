const {default: Bot} = require('el-bot')
const Command = require('./command')

module.exports = function (ctx) {
    const mirai = ctx.mirai
    mirai.on('GroupMessage',message => {
        message.config = ctx.el.bot.danmaku
        Command.match(message)
    })
}
