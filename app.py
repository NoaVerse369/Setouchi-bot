from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

# OpenAI APIキー
openai.api_key = "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"

@app.route("/callback", methods=["POST"])
def callback():
    body = request.get_json()
    print("Request Body:", body)  # LINEから送られたデータを確認するログ

    try:
        # ユーザーからのメッセージを取得
        user_message = body["events"][0]["message"]["text"]
        print("User Message:", user_message)

        # ChatGPTにメッセージを送信して応答を取得
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "あなたは親切なアシスタントです。"},
                {"role": "user", "content": user_message},
            ],
        )
        reply_message = response["choices"][0]["message"]["content"]
    except Exception as e:
        print("Error:", str(e))  # エラーがあればログに出す
        reply_message = "エラーが発生しました。もう一度お試しください。"

    # LINEへの応答データ
    reply_body = {
        "replyToken": body["events"][0]["replyToken"],
        "messages": [{"type": "text", "text": reply_message}],
    }
    print("Reply Body:", reply_body)

    return jsonify(reply_body), 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)
