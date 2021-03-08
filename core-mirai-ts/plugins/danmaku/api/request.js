const axios = require('axios')
const DanmakuApi = axios.create()

DanmakuApi.withCredentials = true; //配置为true

/**
 * 请求拦截
 */
DanmakuApi.interceptors.response.use(response => {
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
  return await DanmakuApi.request({
    url: url,
    method: method,
    params: data
  })
}


module.exports = request
