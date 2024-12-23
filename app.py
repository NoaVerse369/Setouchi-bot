from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["POST"])
def webhook():
    user_message = request.json["events"][0]["message"]["text"]
    return jsonify({
        "replyToken": request.json["events"][0]["replyToken"],
        "messages": [{"type": "text", "text": f"あなたのメッセージ: {user_message}"}]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
