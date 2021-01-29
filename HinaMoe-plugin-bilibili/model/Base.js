// 数据库操作基类


const mysql = require('mysql')
// 创建一个 mysql 连接池
// let poolModule = require('generic-pool');
// let mypool = poolModule.Pool({
//   name: 'mysql',
//   //将建 一个 连接的 handler
//   create: (callback) => {
//     let Client = require('mysql').Client;
//     let c = new Client();
//     c.host = '81.70.25.94'
//     c.port = '3306'
//     c.user = 'root';
//     c.password = 'echoneverdie';
//     c.database = 'bot';
//     c.connect();
//     callback(null, c);
//   },
//   // 释放一个连接的 handler
//   destroy: function (client) {
//     client.end();
//   },
//   // 连接池中最大连接数量
//   max: 10,
//   // 连接池中最少连接数量
//   min: 2,
//   // 如果一个线程3秒钟内没有被使用过的话。那么就释放
//   idleTimeoutMillis: 30000,
//   // 如果 设置为 true 的话，就是使用 console.log 打印入职，当然你可以传递一个 function 最为作为日志记录handler
//   log: true
// })
// mypool.acquire((err,conn) => {
//   if(err){
//     console.log('连接出错')
//   }
// })
const pool = mysql.createPool({
  host: '81.70.25.94',
  user: 'root',
  password: 'echoneverdie',
  database: 'bot'
})

exports.query = function (sql,params){
  return new Promise((resolve, reject) => {
    pool.getConnection((err,conn) => {
      conn.query(sql,params,(err,rows) => {
        if(err){
          reject(err)
        }else{
          resolve(rows)
        }
      })

    })
  })
}

