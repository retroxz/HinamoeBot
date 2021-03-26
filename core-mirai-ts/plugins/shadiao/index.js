const {default: Bot} = require('el-bot')
const {check, Message} = require("mirai-ts");
const COMMAND = ['彩虹屁','朋友圈','毒鸡汤','祖安']
const Api = require('./api')

/**
 * 沙雕语录
 * @param ctx
 */
module.exports =  function (ctx) {
    const mirai = ctx.mirai
    mirai.on('message', async (msg) => { 
        if(check.is(msg.plain, COMMAND)){
            try {
                let data
                if(check.is(msg.plain, COMMAND[0])){
                    data = await Api.getChpWords()
                }else if(check.is(msg.plain, COMMAND[1])){
                    data = await Api.getPyqWords()
                }else if(check.is(msg.plain, COMMAND[2])){
                    data = await Api.getDuWords()
                }else if(check.is(msg.plain, COMMAND[3])){
                    data = await Api.getZaWords()
                }
                if (data.length !== 0) {
                    msg.reply(Message.Plain(data))
                }
            } catch (e) {
                msg.reply(e.message)
            }
        }
    })
}
