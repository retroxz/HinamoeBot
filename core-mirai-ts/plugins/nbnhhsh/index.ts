import Bot from "el-bot";
import {check, Message} from "mirai-ts";
import axios from "axios";

const COMMAND = '/好好说话'

async function guess(text: string) {
    const API_URL = "https://lab.magiconch.com/api/nbnhhsh/guess";
    return axios.post(API_URL, {
        text,
    });
}

/**
 * 能不能好好说话？
 * @param ctx
 */
export default function (ctx: Bot) {
    const mirai = ctx.mirai
    mirai.on('message', async (msg) => {
        try {
            if (check.re(msg.plain, `^${COMMAND}.*`)) {
                const keyword = msg.plain.split(COMMAND)[1].replace(/\s+/g, '')
                if (keyword.search("[\u4e00-\u9fa5]") != -1 || !keyword) {
                    throw new Error("看不懂 嘻嘻")
                }
                const {data} = await guess(keyword);
                let replyMessage = data.length == 0 ? "看不懂 嘻嘻" : `【${keyword}】的意思可能是\n【${data[0].trans.toString()}】`
                console.log(replyMessage)
                // @ts-ignore
                msg.reply([Message.At(msg.sender.id), Message.Plain(replyMessage)])
            }
        } catch (e) {
            msg.reply(e.message)
        }
    })
}
