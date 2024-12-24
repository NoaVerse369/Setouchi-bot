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
        print("Request body:", body)  # リクエスト内容をログに出力

        # 必要なデータがない場合に備えたチェック
        if not body or "events" not in body or not body["events"]:
            print("Invalid request body or no events")
            return "No valid events", 400  # クライアントエラーを返す

        # ユーザーからのメッセージを取得
        user_message = body["events"][0]["message"]["text"]
        print("User message:", user_message)  # ユーザーのメッセージをログに出力

        # OpenAIのAPIを呼び出して返信を生成
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "あなたは親切なアシスタントです。"},
                {"role": "user", "content": user_message},
            ],
        )
        print("OpenAI response:", response)  # OpenAIのレスポンスをログに出力

        # OpenAIのレスポンスから返信内容を抽出
        reply_message = response["choices"][0]["message"]["content"]

        # LINEに返信メッセージを返す形式でデータを整形
        reply_body = {
            "replyToken": body["events"][0]["replyToken"],
            "messages": [{"type": "text", "text": reply_message}],
        }

        print("Reply body:", reply_body)  # LINEへの返信内容をログに出力
        return jsonify(reply_body), 200

    except Exception as e:
        print("Error occurred:", str(e))  # エラー内容をログに出力
        return "Error", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
