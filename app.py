import os
import json
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# 從環境變數讀取
CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# 載入產品資料
with open("products.json", "r", encoding="utf-8") as f:
    PRODUCTS = json.load(f)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text.strip()

    # 第一層選單
    if text in ["選單", "menu"]:
        reply = "請選擇：公司 | 產品 | 制度 | 願景 | 團隊"
    elif text == "公司":
        reply = "Three International 是一家專注健康產品的直銷公司。"
    elif text == "制度":
        reply = "公司制度包含會員制度、獎金制度與銷售獎勵。"
    elif text == "願景":
        reply = "願景：打造全球健康生活品牌。"
    elif text == "團隊":
        reply = "我們的團隊來自各國專業領域，專注健康與事業發展。"

    # 第二層 - 產品清單
    elif text == "產品":
        reply = "請選擇產品名稱：\n" + " | ".join(PRODUCTS.keys())

    # 第三層 - 產品詳細介紹
    elif text in PRODUCTS:
        product = PRODUCTS[text]
        reply = f"📦 {text}\n\n成分：{', '.join(product['成分'])}\n\n介紹：{product['介紹']}"

    else:
        reply = "請輸入『選單』查看功能。"

    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=reply)
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
