import os
import json
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# 環境變數
CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# 載入 JSON 資料
with open("data/products.json", "r", encoding="utf-8") as f:
    data = json.load(f)

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"

# 訊息處理
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_text = event.message.text.strip()
    reply = None

    # --- 公司 ---
    if user_text == "公司":
        reply = "【公司】\n" + data["公司"]["description"]

    # --- 系統 ---
    elif user_text == "系統":
        reply = "【系統】\n" + data["系統"]["description"]

    # --- 團隊 ---
    elif user_text == "團隊":
        reply = "【團隊】\n" + data["團隊"]["description"]
    elif user_text in data["團隊"]:
        reply = f"【團隊 - {user_text}】\n{data['團隊'][user_text]['description']}"

    # --- 產品 ---
    elif user_text in data["產品"]["保健食品"]:
        p = data["產品"]["保健食品"][user_text]
        reply = f"【保健食品 - {user_text}】\n{p['description']}\n\n主要成分:\n" + "\n".join(p["ingredients"])
    elif user_text in data["產品"]["保養品"]["Visage Collection"]:
        p = data["產品"]["保養品"]["Visage Collection"][user_text]
        reply = f"【保養品 - {user_text}】\n{p['description']}\n\n主要成分:\n" + "\n".join(p["ingredients"])
    elif user_text in data["產品"]["飲品"]:
        p = data["產品"]["飲品"][user_text]
        reply = f"【飲品 - {user_text}】\n{p['description']}\n\n主要成分:\n" + "\n".join(p["ingredients"])

    # --- 理念 ---
    elif user_text in data["產品"]["理念"]:
        reply = f"【理念 - {user_text}】\n{data['產品']['理念'][user_text]['description']}"

    # --- 預設回覆 ---
    else:
        reply = "請輸入：公司 / 系統 / 團隊 / 理念 / 產品名稱 (如 Revive, Vitalité, Pure Cleanse, Super Drink)"

    # 回覆訊息
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)