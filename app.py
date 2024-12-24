@app.route("/callback", methods=["POST"])
def callback():
    try:
        # リクエストボディを取得
        body = request.get_json()
        print(f"Request body: {body}")  # リクエストボディをログに出力

        # ユーザーのメッセージを取得
        user_message = body["events"][0]["message"]["text"]
        print(f"User message: {user_message}")  # ユーザーのメッセージをログに出力

        # ChatGPTにリクエスト
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "あなたは親切なアシスタントです。"},
                {"role": "user", "content": user_message},
            ],
        )
        print(f"ChatGPT response: {response}")  # ChatGPTのレスポンスをログに出力

        # ChatGPTのレスポンスを取得
        reply_message = response["choices"][0]["message"]["content"]

        # LINEに返信
        reply_body = {
            "replyToken": body["events"][0]["replyToken"],
            "messages": [{"type": "text", "text": reply_message}],
        }
        print(f"Reply body: {reply_body}")  # 送信する内容をログに出力

        return jsonify(reply_body), 200

    except Exception as e:
        print(f"Error: {e}")  # エラー内容をログに出力
        return "Error", 500
