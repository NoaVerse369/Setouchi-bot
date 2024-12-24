from flask import Flask, request, jsonify
import openai
import os

# OpenAI APIキー設定
openai.api_key = "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"

app = Flask(__name__)

@app.route("/")
def home():
    return "LINE Bot is running!"

@app.route("/callback", methods=["POST"])
def callback():
    body = request.get_json()

    # イベントデータがあるかをチェック
    events = body.get("events", [])
    if not events:
        return "No events found", 200

    # 最初のイベントを取得
    event = events[0]
    if event["type"] != "message" or event["message"]["type"] != "text":
        return "Event type not supported", 200

    user_message = event["message"]["text"]

    try:
        # OpenAIのAPIを使って返信を生成
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "あなたは親切なアシスタントです。"},
                {"role": "user", "content": user_message},
            ],
        )
        reply_message = response["choices"][0]["message"]["content"]

    except Exception as e:
        reply_message = f"エラーが発生しました: {str(e)}"

    # LINEの返信形式に整形
    reply_body = {
        "replyToken": event["replyToken"],
        "messages": [{"type": "text", "text": reply_message}],
    }

    return jsonify(reply_body), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
