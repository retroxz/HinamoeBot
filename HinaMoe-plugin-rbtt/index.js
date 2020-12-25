const {default: Bot} = require('el-bot')
const { Message } = require('mirai-ts')
const path = '.\\resource\\rbtt\\images'
const fs = require('fs')

module.exports = function (ctx) {
  const mirai = ctx.mirai
  mirai.on('GroupMessage',async msg => {
    const id = msg.sender.group.id
    if(ctx.el.config.rbtt.listen.indexOf(id) !==- 1){

      if(msg.plain === '熊兔贴贴'){
        const images = fs.readdirSync(path)
        let fileName = images[Math.floor(Math.random() * images.length)]
        let image = await mirai.api.uploadImage('group',`${path}\\${fileName}`)
        await mirai.api.sendGroupMessage([Message.Image('', image.url,'')], id)
      }
    }
  })
}
