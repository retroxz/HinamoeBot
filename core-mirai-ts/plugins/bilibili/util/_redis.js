// Redis 工具类
const _redis = require('redis')

/**
 * 获取redis连接对象
 * @returns {RedisClient}
 */
exports.client = function () {
    return _redis.createClient(process.env.REDIS_PORT, process.env.REDIS_HOST)
}

exports.setSubscribeInfo = function (id, type) {

}

exports.getSubscribeInfo = function () {

}


