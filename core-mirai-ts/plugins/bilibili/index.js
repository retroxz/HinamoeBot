const {default: Bot} = require('el-bot')
const Commands = require('./util/command')
module.exports = async function (ctx) {
    const mirai = ctx.mirai

    mirai.on('GroupMessage', async msg => {
        Commands.match(msg)
    })
}



