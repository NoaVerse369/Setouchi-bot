from flask import Flask, request, jsonify
import openai
import os

# ChatGPT APIキー設定
openai.api_key = "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"

# Flaskアプリ作成
app = Flask(__name__)

@app.route('/callback', methods=['POST'])
def callback():
    body = request.get_json()
    events = body.get('events', [])

    # LINEからのメッセージイベント
    for event in events:
        if event['type'] == 'message' and event['message']['type'] == 'text':
            user_message = event['message']['text']

            # ChatGPTに問い合わせ
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "あなたは瀬戸内町の情報コンシェルジュです。"},
                    {"role": "user", "content": user_message}
                ]
            )
            reply_message = response['choices'][0]['message']['content']

            # LINEへの返信
            return jsonify({
                "replyToken": event['replyToken'],
                "messages": [{"type": "text", "text": reply_message}]
            })
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
