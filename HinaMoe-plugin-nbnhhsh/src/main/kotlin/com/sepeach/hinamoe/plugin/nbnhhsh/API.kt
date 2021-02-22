package com.sepeach.hinamoe.plugin.nbnhhsh

import com.alibaba.fastjson.JSON
import com.alibaba.fastjson.JSONObject
import kotlinx.serialization.json.JsonArray
import java.util.regex.Pattern

object API {

    private const val  TRANS_URL = "https://lab.magiconch.com/api/nbnhhsh/guess"

    /**
     * @param keyword 关键字
     */
    fun getHhshTrans(keyword: String): Any? {
        val requestJson = """{"text": "$keyword"}""".trimIndent()
        var response = HttpHelper.post(TRANS_URL,requestJson)
        response = (JSON.parseArray(response)[0] as JSONObject)["trans"].toString()
        return response.replace("[","").replace("]","")
            .replace("\"","")
    }
}