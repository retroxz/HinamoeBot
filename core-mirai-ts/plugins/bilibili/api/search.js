// bilibili搜索相关接口
const request = require('./request')

/**
 * 搜索用户
 * @param keyword 关键词
 */
exports.searchUser = async function searchUser(keyword){
  return await request({
    url: 'http://api.bilibili.com/x/web-interface/search/type',
    data: {
      keyword: keyword,
      search_type: 'bili_user',
    }
  })
}
