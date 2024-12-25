from flask import Flask, request, jsonify
import openai

# Flask アプリのインスタンスを作成
app = Flask(__name__)

# OpenAI APIキーを設定
openai.api_key = "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"

# 確認用のエンドポイント
@app.route("/", methods=["GET"])
def home():
    return "LINE Bot is running!"

# LINEのWebhookエンドポイント
@app.route("/callback", methods=["POST"])
def callback():
    try:
        # リクエストボディを取得
        body = request.get_json()
        print("Request body received:", body)  # デバッグ用

        # ユーザーからのメッセージ取得
        user_message = body["events"][0]["message"]["text"]
        print("User message:", user_message)

        # ChatGPTにメッセージを送信して応答を生成
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "あなたは親切なアシスタントです。"},
                {"role": "user", "content": user_message},
            ],
        )
        reply_message = response["choices"][0]["message"]["content"]
        print("Generated reply:", reply_message)

        # LINEの返信形式に変換
        reply_body = {
            "replyToken": body["events"][0]["replyToken"],
            "messages": [{"type": "text", "text": reply_message}],
        }
        return jsonify(reply_body), 200

    except Exception as e:
        print("Error:", str(e))  # エラー内容を出力
        return "Internal Server Error", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
