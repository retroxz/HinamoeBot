@file:Suppress("unused")

package com.sepeach.hinamoe.plugin.spam


import net.mamoe.mirai.console.plugin.jvm.JvmPluginDescription
import net.mamoe.mirai.console.plugin.jvm.KotlinPlugin
import net.mamoe.mirai.console.util.ConsoleExperimentalApi
import net.mamoe.mirai.event.GlobalEventChannel
import net.mamoe.mirai.event.events.GroupMessageEvent
import net.mamoe.mirai.utils.info

object Main : KotlinPlugin(
    @OptIn(ConsoleExperimentalApi::class)
    JvmPluginDescription.loadFromResource()
) {
    // 记录相同消息数量
    private var  sameMessageMap = mutableMapOf<Long,Map<String,*>>()
    private var oldMiraiCode = ""
    override fun onEnable() {
        logger.info { "[Plugin]雏萌复读插件Loaded..." }
        // 注册群消息监听
        GlobalEventChannel.subscribeAlways<GroupMessageEvent> {
            run {
                // 保存消息报文
                val currentMiraiCode = message.serializeToMiraiCode()
                val currentGroupId:Long = sender.group.id
                if(currentMiraiCode != ""){
                    if(currentMiraiCode == sameMessageMap[currentGroupId]?.get("old")){
                        // 保存对应群
                        val currentCount:Int = sameMessageMap[currentGroupId]?.get("count") as Int
                        sameMessageMap[currentGroupId] = mutableMapOf("old" to currentMiraiCode,"count" to currentCount + 1,"chain" to message)
                    }else{
                        oldMiraiCode = currentMiraiCode
                        sameMessageMap[currentGroupId] = mutableMapOf("old" to currentMiraiCode,"count" to 1,"chain" to message)
                    }
                }
                if(sameMessageMap[currentGroupId]?.get("count") == 3){
                    subject.sendMessage(message)
                }
            }
        }
    }
}






