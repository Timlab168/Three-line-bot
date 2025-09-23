import os
import json
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    ImageSendMessage, VideoSendMessage
)

app = Flask(__name__)

# 從環境變數讀取 Token 和 Secret
CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# 讀取產品資料
with open("products.json", "r", encoding="utf-8") as f:
    PRODUCTS = json.load(f)

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_text = event.message.text.strip()

    if user_text == "選單":
        reply_text = "請輸入以下選項：\n公司\n產品\n獎勵\n團隊\n系統"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

    elif user_text == "公司":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="這裡是公司介紹..."))

    elif user_text == "獎勵":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="這裡是獎勵制度..."))

    elif user_text == "團隊":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="這裡是團隊介紹..."))

    elif user_text == "系統":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="這裡是系統介紹..."))

    elif user_text == "產品":
        menu_text = "請輸入以下產品名稱查看詳細資訊：\n"
        menu_text += "\n".join(PRODUCTS.keys())
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=menu_text))

    elif user_text in PRODUCTS:
        product = PRODUCTS[user_text]
        messages = []

        # 1. 產品介紹文字
        if "description" in product:
            messages.append(TextSendMessage(text=product["description"]))

        # 2. 產品圖片
        if "image" in product and product["image"]:
            messages.append(ImageSendMessage(
                original_content_url=product["image"],
                preview_image_url=product["image"]
            ))

        # 3. 產品影片
        if "video" in product and product["video"]:
            messages.append(VideoSendMessage(
                original_content_url=product["video"],
                preview_image_url=product.get("image", "")
            ))

        # 4. 更多資訊連結
        if "link" in product and product["link"]:
            messages.append(TextSendMessage(text=f"更多資訊: {product['link']}"))

        line_bot_api.reply_message(event.reply_token, messages)

    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="我不太明白 😅，請輸入「選單」來查看可選項目。"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)