import os
import json
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# 從環境變數讀取 Token 和 Secret
CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# 載入產品資料
PRODUCTS = {
    "選單": {"成分": "這是測試產品", "介紹": "Bot 已經正常回應！"},
    "hi": {"成分": "greeting", "介紹": "Hello! Bot is alive!"}
}
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    print("Request body:", body)   # Debug log

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("❌ Invalid signature")
        abort(400)

    return "OK"

# 處理文字訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text.strip()
    print("使用者傳來的訊息:", user_message)  # Debug log

    reply = ""

    # 如果輸入 "選單"
    if user_message == "選單":
        reply = "請輸入以下選項之一：\n公司 / 產品 / 制度 / 願景 / 團隊"

    # 如果輸入 "公司"
    elif user_message == "公司":
        reply = "這是一家直銷公司，專注於健康產品。"

    # 如果輸入 "制度"
    elif user_message == "制度":
        reply = "我們的制度採用會員推薦制，詳細內容可向上線確認。"

    # 如果輸入 "產品"
    elif user_message == "產品":
        reply = "請輸入產品名稱，例如：維他命C、魚油"

    # 查詢產品
    elif user_message in PRODUCTS:
        product = PRODUCTS[user_message]
        reply = f"產品名稱: {user_message}\n成分: {product.get('成分', '無')}\n介紹: {product.get('介紹', '無')}"

    # 願景
    elif user_message == "願景":
        reply = "我們的願景是成為全球領先的健康企業。"

    # 團隊
    elif user_message == "團隊":
        reply = "我們的團隊由專業人士組成，專注於產品與會員的發展。"

    else:
        reply = "抱歉，我不太懂您的意思。請輸入『選單』來查看可用選項。"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)