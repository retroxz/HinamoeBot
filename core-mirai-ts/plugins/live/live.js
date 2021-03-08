const axios = require('axios')
const Axios = axios.create()

Axios.withCredentials = true; //配置为true

/**
 * 请求拦截
 */
Axios.interceptors.response.use(response => {
    return response.data
}, error => {
    return Promise.reject(error);
});

/**
 * 基础请求函数
 * @param url string 地址
 * @param data array 请求参数
 * @param method string 请求方式
 * @returns {Promise<void>}
 */
async function request({url, data = {}, method = 'GET'}) {
    return await Axios.request({
        url: url,
        method: method,
        params: data
    })
}

/**
 * 获取直播间信息
 * @param roomId
 * @returns {Promise<void>}
 */
exports.getLiveRoomInfoasync = async function getLiveRoomInfo(roomId) {
    return await request({
        url: `https://api.live.bilibili.com/xlive/web-room/v1/index/getInfoByRoom?room_id=${roomId}`
    })
}


