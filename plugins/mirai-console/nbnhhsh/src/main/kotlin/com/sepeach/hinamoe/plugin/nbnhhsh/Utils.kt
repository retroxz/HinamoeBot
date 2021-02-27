package com.sepeach.hinamoe.plugin.nbnhhsh

import okhttp3.*
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.RequestBody.Companion.asRequestBody
import okhttp3.RequestBody.Companion.toRequestBody
import okio.BufferedSink
import java.io.BufferedInputStream
import java.io.File
import java.io.IOException
import java.util.*
import java.util.concurrent.TimeUnit

object HttpHelper {

    private const val MEDIA_TYPE = "application/json; charset=utf-8"

    private const val MAX_CACHE_SIZE = 1024 * 1024 * 50L// 50M 的缓存大小

    private const val DEFAULT_TIMEOUT = 15L

    /**
     * 获取 OkHttpClient
     */
    private fun getOkHttpClient(): OkHttpClient {
        val builder = OkHttpClient().newBuilder()

        builder.run {
            connectTimeout(DEFAULT_TIMEOUT, TimeUnit.SECONDS)
            readTimeout(DEFAULT_TIMEOUT, TimeUnit.MINUTES)
            writeTimeout(DEFAULT_TIMEOUT, TimeUnit.MINUTES)
            retryOnConnectionFailure(true)
        }

        return builder.build()
    }

    /**
     * 获取键值对FormBody.Builder
     */
    fun getBuilder(): FormBody.Builder {
        return FormBody.Builder()
    }

    /**
     * post方式提交键值对
     * 参数1：[url] url ，参数2：[body] 键值对
     * 返回 可空字符串
     */
    @Throws(IOException::class)
    fun post(url: String, body: RequestBody): String {
        val request = Request.Builder()
                .url(url)
                .post(body)
                .build()
        val response = getOkHttpClient().newCall(request).execute()
        val responseBody = response.body
        return responseBody?.string() ?: ""
    }

    /**
     * post方式提交json字符串
     * 参数1：[url] url，参数2：[json] json字符串
     * 返回可空字符串
     */
    @Throws(IOException::class)
    fun post(url: String, json: String): String {
        ///okHttp4 拓展功能（Kotlin）
        ///String.toMediaType()替换MediaType.get(String)，需要导入import okhttp3.MediaType.Companion.toMediaType
        ///String.toRequestBody(MediaType)替换RequestBody.create(String,MediaType),import okhttp3.RequestBody.Companion.toRequestBody
        return post(
                url,
                json.toRequestBody(MEDIA_TYPE.toMediaType())
        )
    }

    /**
     * post方式提交流
     * 参数1：[url] url，参数2：[bis] 缓冲字节流
     * 返回可空字符串
     */
    @Throws(IOException::class)
    fun post(url: String, bufferedInputStream: BufferedInputStream): String {
        val body = object : RequestBody() {
            override fun writeTo(sink: BufferedSink) {
                try {
                    bufferedInputStream.use { bis ->
                        sink.outputStream().buffered().use { bos ->
                            bis.copyTo(bos)
                        }
                    }
                } catch (e: IOException) {
                    e.printStackTrace()
                }
            }

            override fun contentType(): MediaType {
                return MEDIA_TYPE.toMediaType()
            }

        }
        return post(url, body)
    }

    /**
     * post方式提交文件
     * 参数1：[url] url，参数2：[file] 文件
     * 返回可空字符串
     */
    @Throws(IOException::class)
    fun post(url: String, file: File): String {
        //okHttp4 拓展功能
        //file.asRequestBody需要import okhttp3.RequestBody.Companion.asRequestBody
        //替换RequestBody.create(MediaType.parse("text/x-markdown; charset=utf-8"), file)
        return post(
                url,
                file.asRequestBody("text/x-markdown; charset=utf-8".toMediaType())
        )
    }

    /**
     * Post方式提交分块请求，可以上传多个文件
     * 参数1：[imageUrl] url，参数2：[file] 多个文件
     * 返回可空字符串
     */
    @Throws(IOException::class)
    fun post(url: String, vararg files: File): String {
        val requestBody = MultipartBody.Builder()
                //设置分块提交模式
                .setType(MultipartBody.FORM)
                //分块提交，标题
                .addFormDataPart("title", "block")

        for (file in files) {
            requestBody.addFormDataPart(
                    file.name,
                    file.name,
                    file.asRequestBody("image/png".toMediaType())
            )
        }

        return post(url, requestBody.build())
    }

    /**
     * post方式提交键值对
     * 参数1：[url] url ，参数2：[body] 键值对
     * 返回字符串,如果数据为空抛出空指针异常
     */
    @Throws(IOException::class)
    fun get(url: String): String {
        val request = Request.Builder()
                .url(url)
                .build()

        val response = getOkHttpClient().newCall(request).execute()
        val responseBody = response.body
        return responseBody?.string() ?: ""
    }

    /**
     * 下载文件
     * 参数1：[url] 文件url,参数2：[file] 保存到指定目录
     * 必须在线程中调用，不然主线程会卡住，返回是否下载成功布尔值
     */
    fun downloadFile(url: String, file: File): Boolean {
        val request = Request.Builder()
                .url(url)
                .build()

        try {
            getOkHttpClient().newCall(request).execute().body?.run {
                file.outputStream().buffered().use { bos ->
                    this.byteStream().buffered().use { bis ->
                        bis.copyTo(bos)
                        return true
                    }
                }
            }
        } catch (e: IOException) {
            e.printStackTrace()
        }

        return false
    }




}