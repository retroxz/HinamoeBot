const axios = require('axios')

axios.defaults.withCredentials = true; //配置为true

/**
 * 请求拦截
 */
axios.interceptors.response.use(response => {
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
  return await axios.request({
    url: url,
    method: method,
    params: data
  })
}


exports.getLiveInfo = function (){
  axios.post('https://api.live.bilibili.com/room/v1/Room/get_info', {
    id:22603245
  }).then(function (response) {
    console.log(response)
  })
}

exports.test = async function () {
  // const res = await axios.get('http://api.live.bilibili.com/room/v1/Room/getRoomInfoOld?mid=1265680561')
  this.getLiveInfo()
  // console.log(res.data);
}

module.exports = request
