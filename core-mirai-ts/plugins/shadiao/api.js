const sdAxios =  require("axios");

/**
 * 彩虹屁
 * @returns {Promise<*>}
 */
exports.getChpWords = async function() {
    let res = await sdAxios.get('https://chp.shadiao.app/api.php')
    return res.data
}

/**
 * 朋友圈文案
 * @returns {Promise<*>}
 */
exports.getPyqWords = async function() {
    let res = await sdAxios.get('https://pyq.shadiao.app/api.php')
    return res.data
}

/**
 * 毒鸡汤文案
 * @returns {Promise<*>}
 */
 exports.getDuWords = async function() {
    let res = await sdAxios.get('https://du.shadiao.app/api.php')
    return res.data
}

/**
 * 口吐芬芳
 * @returns {Promise<*>}
 */
 exports.getZaWords = async function() {
    let res = await sdAxios.get('https://nmsl.shadiao.app/api.php?level=min&lang=zh_cn')
    return res.data
}
