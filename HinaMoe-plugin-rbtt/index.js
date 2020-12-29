const {default: Bot} = require('el-bot')
const { Message } = require('mirai-ts')
const path = require('path')
const SEP = path.sep
const imagePath = `.${SEP}${SEP}resource${SEP}${SEP}rbtt${SEP}${SEP}images${SEP}${SEP}`
const fs = require('fs')

module.exports = function (ctx) {

  const mirai = ctx.mirai
  mirai.on('GroupMessage',async msg => {
    const id = msg.sender.group.id
    if(ctx.el.config.rbtt.listen.indexOf(id) !==- 1){

      if(msg.plain === '熊兔贴贴'){
        const images = fs.readdirSync(imagePath)
        let fileName = images[Math.floor(Math.random() * images.length)]
        let image = await mirai.api.uploadImage('group',`${imagePath}${fileName}`)
        await mirai.api.sendGroupMessage([Message.Image('', image.url,'')], id)
      }
    }
  })
}
