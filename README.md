# Three Line Bot

這是一個 LINE Bot，自動回應 Three International 相關資訊。

## 功能
- 輸入 `選單` → 顯示 公司 | 產品 | 制度 | 願景 | 團隊
- 輸入 `公司` → 回覆公司介紹
- 輸入 `產品` → 顯示產品清單
- 輸入 產品名稱 → 顯示成分 + 介紹

## 部署到 Railway
1. Fork 本專案到 GitHub。
2. 登入 [Railway](https://railway.app/)，點「New Project」→「Deploy from GitHub Repo」。
3. 新增環境變數：
   - `CHANNEL_ACCESS_TOKEN`
   - `CHANNEL_SECRET`
4. Railway 會自動部署，複製網址，例如：
   ```
   https://three-line-bot.up.railway.app/callback
   ```
5. 到 LINE Developers → Messaging API → Webhook URL → 貼上並驗證成功。
