const md5 = require('blueimp-md5')
const {default: Bot} = require('el-bot')
const ex = ['大吉', '吉', '半吉', '小吉', '末吉', '凶', '大凶','小凶','吉','末小凶']
const check = require('mirai-ts')

// 生成当前时间日期数据
function generateDate(timestamp) {
  const dateObj = new Date(timestamp * 1000)
  const weekZh = ['日', '一', '二', '三', '四', '五', '六']
  return {
    year: dateObj.getFullYear(),
    month: dateObj.getMonth() + 1,
    date: dateObj.getDate(),
    day: weekZh[dateObj.getDay()]
  }
}

// 获取消息和时间戳
function textMessage(message) {
  let res = {}
  message.messageChain.some(singleMessage => {
    if (singleMessage.type === 'Source') {
      res.timestamp = singleMessage.time
    } else if (singleMessage.type === 'Plain') {
      res.text = singleMessage.text
    }
  })
  return res
}

// 切割求签内容
function splitMessage(message) {
  let messageText = textMessage(message).text
  //去掉空格
  messageText = messageText.replace(/\s+/g,'')
  //切割并取出求签内容
  let text = messageText.split('/求签')[1]
  if(text === ''){
    throw new Error('空的你是要求什么嘛')
  }
  return text
}
// 求签
function fortune(message) {
  // 签所表示的吉凶
  let result = ''
  // 获取到求签内容
  let text = splitMessage(message)
  // 获取到时间日期
  let datetime = generateDate(textMessage(message).timestamp)
  let fortuneText = `${datetime.year}年${datetime.month}月${datetime.date}日 星期${datetime.day}\n${message.sender.memberName}所求内容【${text}】\n`
  // 将求签内容转为md5
  let md5Str = md5(fortuneText)
  // 取md5的第一个数字
  for(let i = 0,len = md5Str.length;i < len;i++){
    if(!isNaN(parseInt(md5Str.substr(i,1)))){
      result = ex[parseInt(md5Str.substr(i,1))]
      break;
    }
  }
  fortuneText = `${fortuneText}【${result}】`
  return fortuneText
}

module.exports = function (ctx) {
  const mirai = ctx.mirai
  mirai.on('GroupMessage', msg => {
    if(check.check.includes(msg.plain, "/求签")){
      try {
        msg.reply(fortune(msg))
      }catch (e) {
        msg.reply(e.message)
      }
    }
  })
}
