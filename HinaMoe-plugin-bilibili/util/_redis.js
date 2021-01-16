// Redis 工具类

const _redis = require('redis')

/**
 * 获取redis连接对象
 * @returns {RedisClient}
 */
exports.client = function () {
  return _redis.createClient(6379,'81.70.25.94')
}

exports.setSubscribeInfo = function (id,type) {

}

exports.getSubscribeInfo = function () {

}


