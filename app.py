from flask import Flask, request, jsonify
import openai
import os

# OpenAI APIキーを設定
openai.api_key = "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"

# Flaskアプリケーションのインスタンスを作成
app = Flask(__name__)

@app.route("/")
def home():
    return "LINE Bot is running!"

@app.route("/callback", methods=["POST"])
def callback():
    try:
        # LINEからのリクエストを取得
        body = request.get_json()

        # メッセージイベントがない場合は終了
        if not body.get("events"):
            return "No events found", 200

        # イベントデータの取得
        event = body["events"][0]
        if event["type"] != "message" or event["message"]["type"] != "text":
            return "Unsupported event type", 200

        user_message = event["message"]["text"]

        # OpenAIのAPIを呼び出して返信を生成
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "あなたは瀬戸内町に関する情報を提供するアシスタントです。"},
                {"role": "user", "content": user_message},
            ]
        )
        reply_message = response["choices"][0]["message"]["content"]

        # LINEに返信メッセージを返す
        reply_body = {
            "replyToken": event["replyToken"],
            "messages": [{"type": "text", "text": reply_message}],
        }

        return jsonify(reply_body), 200

    except Exception as e:
        # エラーレスポンス
        print(f"Error: {str(e)}")
        return "Internal Server Error", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
