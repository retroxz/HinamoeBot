// 弹幕表
const Base = require('./Base')
const Utils = require('../utils')

exports.danmakuRankByDate = async function (currentDate = new Date()) {
    let sql = `SELECT uname AS '昵称',COUNT(*) AS '弹幕量' FROM bili_danmaku WHERE \`timestamp\` > UNIX_TIMESTAMP('${Utils.getCurrentDateString(currentDate)} 00:00:00')* 1000 AND
\`timestamp\` < UNIX_TIMESTAMP( '${Utils.getCurrentDateString(currentDate)} 23:59:59' )* 1000 AND room_id=22603245 GROUP BY uname ORDER BY 弹幕量 DESC LIMIT 10`
    return await Base.query(sql)
}
