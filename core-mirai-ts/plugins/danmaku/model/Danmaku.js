// 弹幕表
const Base = require('./Base')
const Utils = require('../utils')

// 查询弹幕日榜
exports.danmakuRankByDate = async function (currentDate = new Date(),roomId) {
    let sql = `SELECT uname AS '昵称',COUNT(*) AS '弹幕量' FROM bili_danmaku WHERE \`timestamp\` > UNIX_TIMESTAMP('${Utils.getCurrentDateString(currentDate)} 00:00:00')* 1000 AND
\`timestamp\` < UNIX_TIMESTAMP( '${Utils.getCurrentDateString(currentDate)} 23:59:59' )* 1000 AND room_id=${roomId} GROUP BY uid ORDER BY 弹幕量 DESC LIMIT 10`
    return await Base.query(sql)
}
// 随机某人弹幕十条
exports.randomDanmakuByUser = async function (uid,roomId) {
    let sql = `SELECT FROM_UNIXTIME(\`timestamp\`/1000,'%Y-%m-%d') AS 'timestamp',msg FROM bili_danmaku WHERE uid=? AND room_id=? ORDER BY rand() limit 10 `
    return await Base.query(sql, [uid,roomId])
}
