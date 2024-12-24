from flask import Flask, request, jsonify
import openai
import os

# Flask アプリのインスタンスを作成
app = Flask(__name__)

# OpenAI APIキーを設定
openai.api_key = "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"

@app.route("/")
def home():
    return "LINE Bot is running!"  # 起動確認用エンドポイント

@app.route("/callback", methods=["POST"])
def callback():
    # リクエストの内容を取得
    try:
        body = request.get_json()
        print("Request body:", body)  # デバッグ用ログにリクエスト内容を出力

        # LINEからのメッセージイベント
        events = body.get("events", [])
        for event in events:
            print("Event:", event)  # デバッグ用ログにイベント内容を出力

            if event["type"] == "message" and event["message"]["type"] == "text":
                user_message = event["message"]["text"]
                print("User message:", user_message)  # デバッグ用ログにユーザーメッセージを出力

                # ChatGPT APIを使って返信内容を生成
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "あなたは親切なアシスタントです。"},
                        {"role": "user", "content": user_message},
                    ],
                )
                reply_message = response["choices"][0]["message"]["content"]
                print("Reply message:", reply_message)  # デバッグ用ログに応答メッセージを出力

                # LINEに返信
                return jsonify({
                    "replyToken": event["replyToken"],
                    "messages": [{"type": "text", "text": reply_message}],
                })

    except Exception as e:
        print("Error:", str(e))  # デバッグ用ログにエラー内容を出力

    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
