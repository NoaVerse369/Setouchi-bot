from flask import Flask, request, jsonify
import openai
import os

# Flask アプリのインスタンスを作成
app = Flask(__name__)

# OpenAI APIキーを設定
openai.api_key = "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"

@app.route("/")
def home():
    return "LINE Bot is running!"

@app.route("/callback", methods=["POST"])
def callback():
    try:
        # LINEからのリクエストを取得
        body = request.get_json()
        print(f"Request body: {body}")

        # ユーザーからのメッセージを取得
        user_message = body["events"][0]["message"]["text"]

        # OpenAIのAPIを呼び出して返信を生成
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "あなたは瀬戸内町の情報コンシェルジュです。"},
                {"role": "user", "content": user_message},
            ],
        )

        # OpenAIのレスポンスから返信内容を抽出
        reply_message = response["choices"][0]["message"]["content"]

        # LINEに返信メッセージを返す形式でデータを整形
        reply_body = {
            "replyToken": body["events"][0]["replyToken"],
            "messages": [{"type": "text", "text": reply_message}],
        }

        return jsonify(reply_body), 200

    except Exception as e:
        print(f"Error: {e}")
        return "Error occurred", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
