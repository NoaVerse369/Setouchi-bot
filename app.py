from flask import Flask, request, jsonify
import openai

# OpenAI APIキーを設定
openai.api_key = "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"

# Flaskアプリ作成
app = Flask(__name__)

@app.route("/")
def home():
    return "LINE Bot is running!"

@app.route("/callback", methods=["POST"])
def callback():
    body = request.get_json()

    try:
        user_message = body["events"][0]["message"]["text"]

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "あなたは親切で情報豊富なアシスタントです。"},
                {"role": "user", "content": user_message},
            ],
        )

        reply_message = response["choices"][0]["message"]["content"]

        reply_body = {
            "replyToken": body["events"][0]["replyToken"],
            "messages": [{"type": "text", "text": reply_message}],
        }

    except Exception as e:
        reply_body = {
            "replyToken": body["events"][0]["replyToken"],
            "messages": [{"type": "text", "text": f"エラーが発生しました: {str(e)}"}],
        }

    return jsonify(reply_body), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
