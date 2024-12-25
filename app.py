from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

# OpenAI APIキーを設定
openai.api_key = "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"

@app.route("/")
def home():
    return "Bot is running!", 200

@app.route("/callback", methods=["POST"])
def callback():
    try:
        body = request.get_json()
        print("Request body received:", body)

        # イベントがない場合
        if "events" not in body or len(body["events"]) == 0:
            print("No events found in the request body.")
            return jsonify({"status": "no events"}), 400

        # ユーザーメッセージ取得
        event = body["events"][0]
        user_message = event["message"]["text"]
        print("User message received:", user_message)

        # ChatGPTに問い合わせ
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "あなたは親切なアシスタントです。"},
                {"role": "user", "content": user_message}
            ]
        )
        reply_message = response["choices"][0]["message"]["content"]
        print("OpenAI response:", reply_message)

        # LINEへの返信データ
        reply_body = {
            "replyToken": event["replyToken"],
            "messages": [{"type": "text", "text": reply_message}],
        }
        return jsonify(reply_body), 200

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
