import requests

# URL da sua API
url = "https://apipush.onrender.com/send-multiple"

# 🔥 Lista de tokens
tokens = [
    "e_rEUBpi-Gnf0JYt1rXxuG:APA91bF3lPdDc2bfxTddftcPWQTTjvU4aVv7x3MnNGbBa8H61opE0WbCn5ckAbu5iM_xoo5RLwZjElR4P5u0C3tc5GcE-XMtxzRP7X7oWVcKWzFm06XQhYs",
    "cB6rjLbRZH9R_F93CPCIcB:APA91bH2pX-pSc0HEdc8KJQcS9tvZs2vQ47WPwIPcmGljPOZXOvFg4YiHOcRE3VDVNeIZCKl5IeL7rqFnFyoQrfEXNsjnpb5KpAcJLrQwh7m4cTSljkkxa0"
]

data = {
    "tokens": tokens,
    "title": "Teste Python MULTI",
    "body": "Enviando para dois dispositivos 🚀"
}

try:
    response = requests.post(url, json=data)

    print("Status:", response.status_code)
    print("Resposta:", response.text)

except Exception as e:
    print("Erro:", e)