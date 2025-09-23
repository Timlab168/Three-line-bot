import os
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

# 第二層產品選單（先放假資料，之後你可以補 11 個完整內容）
PRODUCTS = {
    "產品A": "這是產品 A 的成分與介紹。",
    "產品B": "這是產品 B 的成分與介紹。",
    "產品C": "這是產品 C 的成分與介紹。"
}

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"

# 文字訊息處理
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_text = event.message.text.strip()

    if user_text == "選單":
        reply_text = "請輸入以下選項：\n公司\n產品\n獎勵\n團隊\n系統"
    elif user_text == "公司":
        reply_text = "這裡是公司介紹：我們是一家致力於健康與成功的國際直銷公司。"
    elif user_text == "獎勵":
        reply_text = "這裡是獎勵制度：多層次獎金設計，激勵合作夥伴成功。"
    elif user_text == "團隊":
        reply_text = "這裡是團隊介紹：團隊合作，共同成長，打造成功。"
    elif user_text == "系統":
        reply_text = "這裡是系統介紹：完善的教育與支援系統，幫助您快速上手。"
    elif user_text == "產品":
        menu_text = "請輸入以下產品名稱查看詳細資訊：\n"
        menu_text += "\n".join(PRODUCTS.keys())
        reply_text = menu_text
    elif user_text in PRODUCTS:
        reply_text = PRODUCTS[user_text]
    else:
        reply_text = "我不太明白 😅，請輸入「選單」來查看可選項目。"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)