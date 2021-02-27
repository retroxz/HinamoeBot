// 数据库操作基类


const mysql = require('mysql')
const pool = mysql.createPool({
    host: process.env.DATABASE_HOST,
    user: process.env.DATABASE_USERNAME,
    password: process.env.DATABASE_PASSWORD,
    database: process.env.DATABASE_NAME
})

exports.query = function (sql, params) {
    return new Promise((resolve, reject) => {
        pool.getConnection((err, conn) => {
            conn.query(sql, params, (err, rows) => {
                if (err) {
                    reject(err)
                } else {
                    resolve(rows)
                }
            })

        })
    })
}

