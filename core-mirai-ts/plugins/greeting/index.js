"use strict";
exports.__esModule = true;
var mirai_ts_1 = require("mirai-ts");
function default_1(ctx) {
    ctx.mirai.on('GroupMessage', function (message) {
        if (mirai_ts_1.check.is(message.plain, ['早', '早安', '早啊', '早呀', '早上好'])) {
            message.reply(goodMorning().toDateString());
        }
    });
}
exports["default"] = default_1;
/**
 * 当说早安的时候
 */
function goodMorning() {
    var currentDate = new Date();
    // 当前小时小于6 归到前一天计算
    if (new Date().getHours() > 6) {
        currentDate.setDate(currentDate.getDate() - 1);
    }
    return currentDate;
}
