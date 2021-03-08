const {Logger} = require("mirai-ts");
const http = require('http')
const createHandler = require('github-webhook-handler')
const logger = new Logger();
let mirai = {}

async function sendMessage({message, groupId}) {
    await mirai.api.sendGroupMessage(message, groupId)
}

exports.start = function (bot) {
    mirai = bot.mirai
    const handler = createHandler({path: '/webhook', secret: bot.el.bot.githook.secret})
    http.createServer(function (req, res) {
        handler(req, res, function (err) {
            res.statusCode = 404
            res.end('NOT FOUND')
        })
    }).listen(bot.el.bot.githook.port)

    logger.success(`GitHook Listen: ${bot.el.bot.githook.port}`)
    logger.success(`GitHook 通知群: ${bot.el.bot.githook.groupId}`)

    handler.on('error', function (err) {
        console.error('Error:', err.message)
    })

    handler.on('push', function (event) {
        console.log('新的Push %s to %s',
            event.payload.repository.name,
            event.payload.ref)
        let message = `仓库[${event.payload.repository.name}]push更新\n分支: ${event.payload.ref}\n提交人: ${event.payload.pusher.name}(${event.payload.pusher.email})\n提交信息: ${event.payload.head_commit.message}\n${event.payload.repository.url}`
        sendMessage({
            message,
            groupId: bot.el.bot.githook.groupId
        })
    })

    handler.on('issues', function (event) {
        console.log('仓库[%s]收到新的[issue] action=%s: #%d %s',
            event.payload.repository.name,
            event.payload.action,
            event.payload.issue.number,
            event.payload.issue.title)
        let message = `仓库[${event.payload.repository.name}]issue更新\n类型: ${event.payload.action}\n标题: ${event.payload.issue.number}${event.payload.issue.title}\n地址: ${event.payload.issue.html_url}`
        sendMessage({
            message,
            groupId: bot.el.bot.githook.groupId
        })
    })

    handler.on('commit_comment', function (event) {
        console.log(event)
    })
}
