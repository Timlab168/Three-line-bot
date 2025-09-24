import json
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# ===== Line Bot 設定 =====
line_bot_api = LineBotApi("你的CHANNEL_ACCESS_TOKEN")
handler = WebhookHandler("你的CHANNEL_SECRET")

# ===== 載入產品資料 =====
with open("products.json", "r", encoding="utf-8") as f:
    products = json.load(f)

# ===== Webhook 路由 =====
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"

# ===== 處理訊息 =====
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_msg = event.message.text.strip()

    reply_text = "我還不太明白您的需求，可以再說明嗎？"

    # 查詢產品
    for category, items in products.items():
        for item in items:
            if user_msg in item["name"]:
                reply_text = f"{item['name']}：\n{item['description']}"
                break

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

# ===== 主程式 =====
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
