// bilibili个人空间相关接口
const request = require('./request')

/**
 * 获取用户信息
 * @param mid 用户uid
 * @returns {Promise<void>}
 */
exports.spaceInfo = async function spaceInfo(mid) {
  return await request({
    url: 'http://api.bilibili.com/x/space/acc/info',
    data: {mid}
  })
}

/**
 * 获取用户信息(卡片)
 * @param mid 用户uid
 * @returns {Promise<void>}
 */
exports.spaceInfoWithFans = async function spaceInfoWithFans(mid) {
  return await request({
    url: 'http://api.bilibili.com/x/web-interface/card',
    data: {mid}
  })
}
