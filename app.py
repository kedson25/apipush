from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, messaging
import os
import json

app = Flask(__name__)

# 🔐 Firebase credentials (Render env)
firebase_json = os.environ.get("FIREBASE_CREDENTIALS")

if not firebase_json:
    raise Exception("FIREBASE_CREDENTIALS não configurado")

cred_dict = json.loads(firebase_json)

if not firebase_admin._apps:
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)


# 🌐 Imagem (aparece dentro da notificação, NÃO é ícone)
IMAGE_URL = "https://i.ibb.co/0RdkwbvT/agendar-4.png"


# -------------------------
# 🏠 TESTE
# -------------------------
@app.route("/", methods=["GET"])
def home():
    return "API rodando no Render 🚀"


# -------------------------
# 📱 PUSH INDIVIDUAL
# -------------------------
@app.route("/send", methods=["POST"])
def send_notification():
    data = request.json

    token = data.get("token")
    title = data.get("title")
    body = data.get("body")

    if not token or not title or not body:
        return jsonify({"error": "Campos obrigatórios"}), 400

    message = messaging.Message(
        token=token,

        notification=messaging.Notification(
            title=title,
            body=body
        ),

        android=messaging.AndroidConfig(
            priority="high",
            notification=messaging.AndroidNotification(
                sound="default",
                channel_id="default",
                icon="ic_notification",  # 🔥 ÍCONE LOCAL DO ANDROID
                color="#FF0000",
                image=IMAGE_URL  # 🖼️ imagem no corpo da notificação
            )
        ),

        data={
            "title": title,
            "body": body,
            "image": IMAGE_URL,
            "click_action": "FLUTTER_NOTIFICATION_CLICK"
        }
    )

    try:
        response = messaging.send(message)
        return jsonify({"success": True, "message_id": response})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# -------------------------
# 📡 PUSH MÚLTIPLO
# -------------------------
@app.route("/send-multiple", methods=["POST"])
def send_multiple():
    data = request.json

    tokens = data.get("tokens", [])
    title = data.get("title")
    body = data.get("body")

    if not tokens or not title or not body:
        return jsonify({"error": "Campos obrigatórios"}), 400

    unique_tokens = list(set(tokens))

    success = 0
    failed = 0
    errors = []

    for token in unique_tokens:
        message = messaging.Message(
            token=token,

            notification=messaging.Notification(
                title=title,
                body=body
            ),

            android=messaging.AndroidConfig(
                priority="high",
                notification=messaging.AndroidNotification(
                    sound="default",
                    channel_id="default",
                    icon="ic_notification",  # 🔥 ÍCONE LOCAL
                    color="#FF0000",
                    image=IMAGE_URL  # 🖼️ imagem opcional
                )
            ),

            data={
                "title": title,
                "body": body,
                "image": IMAGE_URL
            }
        )

        try:
            messaging.send(message)
            success += 1
        except Exception as e:
            failed += 1
            errors.append(str(e))

    return jsonify({
        "success": True,
        "sent": success,
        "failed": failed,
        "errors": errors
    })


# -------------------------
# 🚀 START
# -------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
