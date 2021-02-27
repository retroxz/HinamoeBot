@file:Suppress("unused")

package com.sepeach.hinamoe.plugin.fortune

import com.github.heqiao2010.lunar.LunarCalendar
import net.mamoe.mirai.Bot
import net.mamoe.mirai.console.plugin.jvm.JvmPluginDescription
import net.mamoe.mirai.console.plugin.jvm.KotlinPlugin
import net.mamoe.mirai.console.util.ConsoleExperimentalApi
import net.mamoe.mirai.event.GlobalEventChannel
import net.mamoe.mirai.event.subscribeGroupMessages
import net.mamoe.mirai.message.data.PlainText
import net.mamoe.mirai.utils.*
import java.security.MessageDigest
import java.text.SimpleDateFormat
import java.util.*
import java.util.regex.Pattern
import java.math.BigInteger

val ex = arrayOf("大吉", "吉", "半吉", "小吉", "末吉", "凶", "大凶", "小凶", "吉", "末凶")
val weekDays = arrayOf("星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六")
val today = Calendar.getInstance()
val lunar = LunarCalendar.solar2Lunar(today)

object FortuneMain : KotlinPlugin(
        @OptIn(ConsoleExperimentalApi::class)
        JvmPluginDescription.loadFromResource()
) {
    private lateinit var targetBot: Bot
    override fun onEnable() {
        logger.info { "HinaMoe 求签插件已加载" }

        // 监听群消息
        GlobalEventChannel.subscribeGroupMessages {
            startsWith("/求签") {
                // 获取到纯消息文本
                try {
                    val currentDate = Date()
                    var content = message.filterIsInstance<PlainText>().firstOrNull().toString()
                    content = Pattern.compile("\\s*|\t|\r|\n").matcher(content).replaceAll("")
                    val splitArr = content.split("/求签")
                    val fortuneMsg = splitArr[splitArr.size - 1].trim()
                    if (fortuneMsg == "")
                        logger.info("空的你是要干嘛？想打架吗？？？")
                    val result = generateFortune("${SimpleDateFormat("yyyy年MM月dd日").format(currentDate)}-${fortuneMsg}-${sender.id}")
                    val resultMessage = """
                     ${SimpleDateFormat("yyyy年MM月dd日").format(currentDate)}（${lunar.fullLunarName.substring(5)}） ${weekDays[today.get(Calendar.DAY_OF_WEEK)]}
                     ${senderName}所求内容【${fortuneMsg}】
                     【${result}】
                 """.trimIndent()
                    subject.sendMessage(resultMessage)
                } catch (e: java.lang.Exception) {
                    subject.sendMessage(e.message.toString())
                }
            }
        }
    }
}

/**
 * 将消息字符串转换成签
 */
fun generateFortune(value: String): String {
    val md5: String? = md5Encryption(value)
    var i = 0
    var index: Int = 0
    while (i < md5?.length!!) {
        try {
            index = md5.substring(md5.length - 1 - i, md5.length - i).toInt()
        } catch (e: java.lang.NumberFormatException) {
            i++
            continue
        }
        break

    }
    return ex[index]
}

fun md5Encryption(value: String): String? {
    val md: MessageDigest = MessageDigest.getInstance("md5")
    val bytes = md.digest(value.toByteArray(charset("utf-8")))
    return BigInteger(1, bytes).toString()
}
