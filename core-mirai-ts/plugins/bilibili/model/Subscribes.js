// 订阅表
const Base = require('./Base')
const Util = require("../util/util");

/**
 * 新增
 * @param params
 * @returns {Promise<unknown>}
 */
exports.add = async function (params) {
    let sql = "INSERT INTO `bot_subscribes`( `qid`, `qnick`, `type`, `qtype`, `uid`, `room_id`, `nick_name`, `operator_id`, `operator_nick`, `create_time`) " +
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
    return await Base.query(sql, [params.qid, params.qnick, params.type, params.qtype, params.uid, params.roomId, params.nick, params.operatorId, params.operatorNick, params.createTime])
}

/**
 * 查询某个订阅是否存在
 * @param filed
 * @param type
 * @param groupId
 * @param uid
 * @returns {Promise<unknown>}
 */
exports.querySubscribeExist = async function ({filed = '*', type, groupId, uid}) {
    let sql = `SELECT ${filed} FROM bot_subscribes WHERE type=? AND qid=? AND uid LIKE ? AND delete_time=0`
    return await Base.query(sql, [type, groupId, uid])
}

/**
 * 删除某个订阅
 * @param type
 * @param groupId
 * @param uid
 * @returns {Promise<any>}
 */
exports.deleteSubscribeExist = async function ({type, groupId, uid}) {
    let sql = `UPDATE bot_subscribes SET delete_time='${Util.getCurrentDateString()}' WHERE type=? AND qid=? AND uid=? `
    return await Base.query(sql, [type, groupId, uid])
}
