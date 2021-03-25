const axios =  require("axios");

/**
 * 整晚安祝福
 * @returns {Promise<*>}
 */
exports.getNightWords = async function() {
    let res = await axios.get('https://el-bot-api.vercel.app/api/words/wanan')
    return res.data[0]
}

/**
 * 整正能量语句
 * @returns {Promise<*>}
 */
exports.getYoungWords = async function() {
    let res = await axios.get('https://el-bot-api.vercel.app/api/words/young')
    return res.data[0]
}
