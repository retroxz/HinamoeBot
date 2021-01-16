// bilibili个人空间相关接口
const request = require('./request')

/**
 * 获取用户信息
 * @param mid
 * @returns {Promise<void>}
 */
exports.spaceInfo = async function spaceInfo(mid) {
  return await request({
    url: 'http://api.bilibili.com/x/space/acc/info',
    data: {mid}
  })
}
