from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# OpenAI APIキーを環境変数から取得（環境変数がない場合は直接キーをここに記載）
openai.api_key = os.getenv("OPENAI_API_KEY", "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")

@app.route("/")
def home():
    return "LINE Bot is running!"

@app.route("/callback", methods=["POST"])
def callback():
    try:
        body = request.get_json()
        events = body.get("events", [])

        # メッセージイベントがあるか確認
        if not events or not events[0].get("message"):
            return "No message event", 200

        event = events[0]
        user_message = event["message"]["text"]

        # ChatGPT APIへの問い合わせ
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "あなたは瀬戸内町の情報コンシェルジュです。"},
                {"role": "user", "content": user_message},
            ],
        )
        reply_message = response["choices"][0]["message"]["content"]

        # LINEへの返信データを準備
        reply_body = {
            "replyToken": event["replyToken"],
            "messages": [{"type": "text", "text": reply_message}],
        }

        return jsonify(reply_body), 200

    except Exception as e:
        # エラーの場合に内容をログとして表示
        print(f"Error: {str(e)}")
        return f"Error: {str(e)}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
