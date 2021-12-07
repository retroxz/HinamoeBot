const mysql = require('mysql')
const pool = mysql.createPool({
    host: process.env.DATABASE_HOST,
    port: process.env.DATABASE_PORT,
    user: process.env.DATABASE_USERNAME,
    password: process.env.DATABASE_PASSWORD,
    database: process.env.BOT_DATABASE
})

exports.query = function (sql, params) {
    return new Promise((resolve, reject) => {
        pool.getConnection((err, conn) => {
            conn.query(sql, params, (err, rows) => {
                if (err) {
                    reject(err)
                    conn.release()
                } else {
                    resolve(rows)
                    conn.release()
                }
            })

        })
    })
}
