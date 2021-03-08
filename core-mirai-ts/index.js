const { default: Bot } = require("el-bot");
const el = require("./el");
const GitHook = require("./el/githook")

// @ts-ignore
const bot = new Bot(el);
bot.start().then(() => {
    // 启动GitHook
    GitHook.start(bot)
})

// 监听消息
bot.mirai.on("message", (msg) => {
  log(msg)
})


function log(message){
  switch (message.type){
    case 'GroupMessage':
      console.log(`[${formatTimestamp(message.messageChain[0].time)}] ${message.sender.memberName}(${message.sender.id}): ${message.plain} 来自群:${message.sender.group.name}(${message.sender.group.id})`)
      break
    case 'FriendMessage':
      console.log(`[${formatTimestamp(message.messageChain[0].time)}] ${message.sender.nickname}(${message.sender.id}): ${message.plain}`)
      break
  }
}

function formatTimestamp(timestamp){
  const date = new Date(timestamp*1000)
  return `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()} ${date.getHours()}:${date.getMinutes()}:${date.getSeconds()}`
}
