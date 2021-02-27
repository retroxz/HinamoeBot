@file:Suppress("unused")

package com.sepeach.hinamoe.plugin.nbnhhsh

import net.mamoe.mirai.console.plugin.jvm.JvmPluginDescription
import net.mamoe.mirai.console.plugin.jvm.KotlinPlugin
import net.mamoe.mirai.console.util.ConsoleExperimentalApi
import net.mamoe.mirai.event.GlobalEventChannel
import net.mamoe.mirai.event.subscribeGroupMessages
import net.mamoe.mirai.message.data.At
import net.mamoe.mirai.message.data.PlainText
import net.mamoe.mirai.utils.info
import java.util.regex.Pattern


// 定义主类方法 2, 使用 `JvmPluginDescription.loadFromResource()` 从 resources/plugin.yml 加载

object Main : KotlinPlugin(
    @OptIn(ConsoleExperimentalApi::class)
    JvmPluginDescription.loadFromResource()
) {
    override fun onEnable() {
        logger.info { "[Plugin]雏萌好好说话插件Loaded..." }
        // 监听群消息
        GlobalEventChannel.subscribeGroupMessages {
            startsWith("/好好说话") {
                try {
                    var content = Pattern.compile("\\s*|\t|\r|\n")
                        .matcher(message.filterIsInstance<PlainText>().firstOrNull().toString()).replaceAll("").replace("\"","")
                    val hhshMsg = content.split("/好好说话")
                    val keyword = hhshMsg[hhshMsg.size - 1]
                    if (keyword == "" || Pattern.compile("[\\u4e00-\\u9fa5]").matcher(keyword).find())
                        throw Exception()
                    // 请求API
                    val start = System.currentTimeMillis();
                    val result = API.getHhshTrans(keyword)
                    if(result == "null"){
                        throw Exception()
                    }
                    val replyMessage = """
                    【$keyword】的意思可能是
                    【$result】
                """.trimIndent()
                    subject.sendMessage(At(sender.id) + replyMessage)
                } catch (e: Exception) {
                    subject.sendMessage(At(sender.id) + "看不懂 嘻嘻")
                }
            }
        }
    }
}