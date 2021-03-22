// 弹幕表
const Base = require('./Base')

// const Utils = require('../utils')


exports.queryGreetingLog = async function ({groupId, senderId, type}) {
    let sql = "SELECT rank FROM greeting_log WHERE create_time BETWEEN ? AND ? AND group_id=? AND sender_id=? AND type=?"
    let currentDate = new Date()
    let startDateTime = `${currentDate.getFullYear()}-${currentDate.getMonth() + 1}-${currentDate.getDate()} 0:00:00`
    let endDateTime = `${currentDate.getFullYear()}-${currentDate.getMonth() + 1}-${currentDate.getDate()} 23:59:59`
    return await Base.query(sql,[startDateTime,endDateTime,groupId,senderId,type])
}
exports.addGreetingLog = async function ({groupId,groupName,senderId,senderName,type,morning_time,create_time}) {
    let currentDate = new Date()
    let startDateTime = `${currentDate.getFullYear()}-${currentDate.getMonth() + 1}-${currentDate.getDate()} 0:00:00`
    let endDateTime = `${currentDate.getFullYear()}-${currentDate.getMonth() + 1}-${currentDate.getDate()} 23:59:59`
    let greetingLog = await this.queryGreetingLog({groupId,senderId,type})
    if(greetingLog.length > 0){
        return -1
    }
    let sql = "INSERT INTO greeting_log(group_id,group_name,sender_id,sender_name,type,morning_time,create_time,rank)" +
        "VALUES(?,?,?,?,?,?,?,(SELECT * FROM (SELECT COUNT(*) FROM greeting_log WHERE create_time BETWEEN ? AND ? AND group_id=? AND type=?)AS t1) +1 )"
    await Base.query(sql,
        [groupId,groupName,senderId,senderName,type,morning_time,create_time,startDateTime,endDateTime,groupId,type])
    let res = await this.queryGreetingLog({groupId, senderId, type})
    return res[0]['rank']
}
exports.queryLastGreetingLog = async function({groupId, senderId, type}){
    let sql = "SELECT * FROM greeting_log WHERE group_id=? AND sender_id=? AND type=? ORDER BY create_time DESC LIMIT 1"
    let res = await Base.query(sql,[groupId,senderId,type])
    return res
}
