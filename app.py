from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# OpenAI APIキー
openai.api_key = "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"

@app.route("/callback", methods=["POST"])
def callback():
    body = request.get_json()
    print("Request body received:", body)  # LINEからのリクエスト内容を確認
    
    try:
        user_message = body["events"][0]["message"]["text"]
        print("User message:", user_message)  # ユーザーが送ったメッセージ

        # OpenAIへのリクエスト
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "あなたは親切なアシスタントです。"},
                {"role": "user", "content": user_message},
            ],
        )
        print("OpenAI response:", response)  # OpenAIからのレスポンス
        
        reply_message = response["choices"][0]["message"]["content"]
    except Exception as e:
        print("Error while generating response:", str(e))  # エラー内容を確認
        reply_message = "エラーが発生しました。もう一度お試しください。"

    reply_body = {
        "replyToken": body["events"][0]["replyToken"],
        "messages": [{"type": "text", "text": reply_message}],
    }
    print("Reply body:", reply_body)  # LINEに送るデータ内容
    
    return jsonify(reply_body), 200

if __name__ == "__main__":
    # Render が使用するポートを指定
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
