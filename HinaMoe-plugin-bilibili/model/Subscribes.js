// 订阅表
const Base = require('./Base')


exports.add = async function (params) {
  let sql = "INSERT INTO `bot_subscribes`( `qid`, `qnick`, `type`, `qtype`, `uid`, `room_id`, `nick_name`, `operator_id`, `operator_nick`, `create_time`) " +
    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
  return await Base.query(sql, [params.qid, params.qnick, params.type, params.qtype, params.uid, params.roomId, params.nick, params.operatorId, params.operatorNick, params.createTime])
}
