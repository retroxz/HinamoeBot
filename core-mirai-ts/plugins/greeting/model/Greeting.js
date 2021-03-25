// 弹幕表
const Base = require('./Base')

// const Utils = require('../utils')


exports.queryGreetingLog = async function ({groupId, senderId, type}) {
    let sql = "SELECT rank FROM greeting_log WHERE create_time BETWEEN ? AND ? AND group_id=? AND sender_id=? AND type=?"
    let currentDate = new Date()
    let startDateTime = getStartDateTime(currentDate)
    let endDateTime = getEndDateTime(currentDate)
    return await Base.query(sql,[startDateTime,endDateTime,groupId,senderId,type])
}
exports.addGreetingLog = async function ({groupId,groupName,senderId,senderName,type,morning_time,create_time}) {
    let currentDate = new Date()
    let startDateTime = getStartDateTime(currentDate)
    let endDateTime = getEndDateTime(currentDate)
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
    let sql = "SELECT * FROM greeting_log WHERE create_time BETWEEN ? AND ? AND group_id=? AND sender_id=? AND type=? ORDER BY create_time DESC LIMIT 1"
    let currentDate = getNextDate(new Date(), -1)
    let startDateTime = getStartDateTime(currentDate)
    let endDateTime = getEndDateTime(currentDate)
    let res = await Base.query(sql,[startDateTime,endDateTime,groupId,senderId,type])
    return res
}

exports.queryLastSleep = async function(){
    let currentDate = new Date()
    let startDateTime = getStartDateTime(currentDate)
    let endDateTime = getEndDateTime(currentDate)
    let sql = "SELECT group_id,sender_id,sender_name,create_time FROM greeting_log WHERE ( group_id, create_time ) IN ( SELECT group_id,max( create_time ) FROM greeting_log WHERE create_time BETWEEN ? AND ? AND type = 2 GROUP BY group_id)"
    return await Base.query(sql,[startDateTime,endDateTime])
}

function getNextDate(date, day){
    let dd = new Date(date)
    dd.setDate(dd.getDate() + day)
    let y = dd.getFullYear()
    let m = dd.getMonth() + 1 < 10 ? "0" + (dd.getMonth() + 1) : dd.getMonth() + 1
    let d = dd.getDate() < 10 ? "0" + dd.getDate() : dd.getDate()
    let changeDate = y + "-" + m + "-" + d
    return new Date(changeDate)
}

function getStartDateTime(currentDate){
    let startDateTime, date
    if(currentDate.getHours() < 6){
        date = getNextDate(currentDate, -1)
        startDateTime = `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()} 6:00:00`
    }else {
        startDateTime = `${currentDate.getFullYear()}-${currentDate.getMonth() + 1}-${currentDate.getDate()} 6:00:00`
    }
    return startDateTime
}

function getEndDateTime(currentDate){
    let endDateTime, date
    if(currentDate.getHours() < 6){
        date = getNextDate(currentDate, -1)
        endDateTime = `${currentDate.getFullYear()}-${currentDate.getMonth() + 1}-${currentDate.getDate()} 5:59:59`
    }else {
        date = getNextDate(currentDate, 1)
        endDateTime = `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()} 5:59:59`
    }
    return endDateTime
}
