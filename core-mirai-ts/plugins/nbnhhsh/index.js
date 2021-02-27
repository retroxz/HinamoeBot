"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
exports.__esModule = true;
var mirai_ts_1 = require("mirai-ts");
var axios_1 = require("axios");
var COMMAND = '/好好说话';
function guess(text) {
    return __awaiter(this, void 0, void 0, function () {
        var API_URL;
        return __generator(this, function (_a) {
            API_URL = "https://lab.magiconch.com/api/nbnhhsh/guess";
            return [2 /*return*/, axios_1["default"].post(API_URL, {
                    text: text
                })];
        });
    });
}
/**
 * 能不能好好说话？
 * @param ctx
 */
function default_1(ctx) {
    var _this = this;
    var cli = ctx.cli;
    var mirai = ctx.mirai;
    mirai.on('message', function (msg) { return __awaiter(_this, void 0, void 0, function () {
        var keyword, data, replyMessage, e_1;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    _a.trys.push([0, 3, , 4]);
                    if (!mirai_ts_1.check.re(msg.plain, "^" + COMMAND + ".*")) return [3 /*break*/, 2];
                    keyword = msg.plain.split(COMMAND)[1].replace(/\s+/g, '');
                    if (keyword.search("[\u4e00-\u9fa5]") != -1 || !keyword) {
                        throw new Error("看不懂 嘻嘻");
                    }
                    return [4 /*yield*/, guess(keyword)];
                case 1:
                    data = (_a.sent()).data;
                    replyMessage = data.length == 0 ? "看不懂 嘻嘻" : "\u3010" + keyword + "\u3011\u7684\u610F\u601D\u53EF\u80FD\u662F\n\u3010" + data[0].trans.toString() + "\u3011";
                    console.log(replyMessage);
                    // @ts-ignore
                    msg.reply([mirai_ts_1.Message.At(msg.sender.id), mirai_ts_1.Message.Plain(replyMessage)]);
                    _a.label = 2;
                case 2: return [3 /*break*/, 4];
                case 3:
                    e_1 = _a.sent();
                    msg.reply("看不懂 嘻嘻");
                    return [3 /*break*/, 4];
                case 4: return [2 /*return*/];
            }
        });
    }); });
    /*cli
      .command("nbnhhsh <text...>")
      .description("能不能好好说话？")
      .action(async (text: string[]) => {
        const msg = ctx.mirai.curMsg as MessageType.ChatMessage;
        try {
          const { data } = await guess(text.join(","));
          if (data.length) {
            data.forEach((result: any) => {
              let content = `${result.name} 理解不能`;
              if (result.trans && result.trans.length > 0) {
                content = `${result.name} 的含义：${result.trans.join("，")}`;
              } else if (result.inputting && result.inputting.length > 0) {
                content = `${result.name} 有可能是：${result.inputting.join(
                  "，"
                )}`;
              }
              msg.reply(content);
            });
          }
        } catch (e) {
          msg.reply(e.message);
        }
      });*/
}
exports["default"] = default_1;
