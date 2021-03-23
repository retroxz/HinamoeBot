const {default: Bot} = require('el-bot')
const Help = require('./help')

module.exports = function (ctx){
    ctx.mirai.on('message',message => {
        Help.match(message)
    })
}

