const { Mirai, Logger } = require("mirai-ts");
const http = require('http')
const createHandler = require('github-webhook-handler')
const YAML = require('yamljs');
const logger = new Logger();


const mahConfig = JSON.parse(JSON.stringify(YAML.load('./config/http.yml')))
const gitHookConfig = JSON.parse(JSON.stringify(YAML.load('./config/app.yml')))
const qq = parseInt(gitHookConfig.githook.qq);

const mirai = new Mirai(mahConfig);
async function sendMessage(message) {
    await mirai.link(qq);
    await mirai.api.sendGroupMessage(message,gitHookConfig.githook.groupId)
}

exports.start = function (){
    const handler = createHandler({ path: '/webhook', secret: gitHookConfig.githook.secret })
    http.createServer(function (req, res) {
        handler(req, res, function (err) {
            res.statusCode = 404
            res.end('no such location')
        })
    }).listen(gitHookConfig.githook.port)

    logger.success(`GitHook Listen: ${gitHookConfig.githook.port}`)
    logger.success(`GitHook 通知群: ${gitHookConfig.githook.groupId}`)

    handler.on('error', function (err) {
        console.error('Error:', err.message)
    })

    handler.on('push', function (event) {
        console.log('Received a push event for %s to %s',
            event.payload.repository.name,
            event.payload.ref)
        let message = `仓库[${event.payload.repository.name}]push更新\n分支: ${event.payload.ref}\n提交人: ${event.pusher.name}(${event.pusher.email})\n提交信息: ${event.head_commit.message}\n${repository.url}`
        sendMessage(message)
    })

    handler.on('issues', function (event) {
        console.log('仓库[%s]收到新的[issue] action=%s: #%d %s',
            event.payload.repository.name,
            event.payload.action,
            event.payload.issue.number,
            event.payload.issue.title)
        let message = `仓库[${event.payload.repository.name}]issue更新\n类型: ${event.payload.action}\n标题: ${event.payload.issue.number}${event.payload.issue.title}\n地址: ${event.payload.issue.html_url}`
        sendMessage(message)
    })

    handler.on('commit_comment',function (event){
        console.log(event)
    })
}
