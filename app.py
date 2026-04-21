from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, messaging
import os
import json

app = Flask(__name__)

# 🔐 Firebase via variável de ambiente (RECOMENDADO no Render)
firebase_json = os.environ.get("FIREBASE_CREDENTIALS")

if not firebase_json:
    raise Exception("FIREBASE_CREDENTIALS não configurado")

cred_dict = json.loads(firebase_json)
cred = credentials.Certificate(cred_dict)

firebase_admin.initialize_app(cred)


@app.route("/", methods=["GET"])
def home():
    return "API rodando no Render 🚀"


@app.route("/send", methods=["POST"])
def send_notification():
    data = request.json

    token = data.get("token")
    title = data.get("title")
    body = data.get("body")

    if not token or not title or not body:
        return jsonify({"error": "Campos obrigatórios: token, title, body"}), 400

    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body
        ),
        token=token
    )

    try:
        response = messaging.send(message)
        return jsonify({
            "success": True,
            "message_id": response
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/send-multiple", methods=["POST"])
def send_multiple():
    data = request.json

    tokens = data.get("tokens")
    title = data.get("title")
    body = data.get("body")

    if not tokens or not title or not body:
        return jsonify({"error": "Campos obrigatórios: tokens, title, body"}), 400

    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=title,
            body=body
        ),
        tokens=tokens
    )

    try:
        response = messaging.send_multicast(message)
        return jsonify({
            "success": True,
            "success_count": response.success_count,
            "failure_count": response.failure_count
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)