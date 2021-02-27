// bilibili直播相关接口
const request = require('./request')

/**
 * 获取直播间信息 以直播间房间号为准
 * @param id int 直播间id
 * @returns {Promise<void>}
 */
exports.roomInfo = async function roomInfo(id) {
  return await request({
    url: 'https://api.live.bilibili.com/room/v1/Room/get_info',
    data: {id}
  })
}
