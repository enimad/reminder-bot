import requests
import time
from datetime import datetime

BOT_TOKEN = "7976747374:AAG0Xf1vFrlpdNc1NgwYhfJ2ZrBXSh4dyIg"
CHAT_ID = "8002317409"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# État de la confirmation
confirmed_today = False
last_sent_message_id = None

# Message d’amour 💖
def send_reminder():
    global last_sent_message_id
    text = "Coucou mon amour 💖\nN'oublie pas de prendre ton médicament 💊\nClique sur le bouton quand c’est fait ✨"
    keyboard = {
        "inline_keyboard": [[{
            "text": "Confirmé ✅",
            "callback_data": "confirmed"
        }]]
    }
    response = requests.post(f"{API_URL}/sendMessage", json={
        "chat_id": CHAT_ID,
        "text": text,
        "reply_markup": keyboard
    })
    result = response.json()
    if "result" in result:
        last_sent_message_id = result["result"]["message_id"]

# Vérifie si le bouton a été cliqué
def check_confirmation():
    global confirmed_today
    updates = requests.get(f"{API_URL}/getUpdates").json()
    for update in updates.get("result", []):
        if "callback_query" in update:
            data = update["callback_query"]["data"]
            if data == "confirmed":
                confirmed_today = True
                # Envoie un message de félicitations 🥳
                requests.post(f"{API_URL}/sendMessage", json={
                    "chat_id": CHAT_ID,
                    "text": "Bravo mon cœur ❤️ Merci d’avoir pris ton médicament 🥰"
                })
                # Supprime la notification de rappel
                callback_id = update["callback_query"]["id"]
                requests.post(f"{API_URL}/answerCallbackQuery", json={
                    "callback_query_id": callback_id,
                    "text": "C'est noté mon amour 💕"
                })
                break

# Boucle principale
while True:
    now = datetime.now()
if now.minute % 1 == 0 and not confirmed_today:
        send_reminder()
        for i in range(6):  # 6 rappels toutes les 10 minutes = 1 heure
            for j in range(5):
    time.sleep(2)  # Check toutes les 2 secondes
                check_confirmation()
                if confirmed_today:
                    break
            if confirmed_today:
                break
            send_reminder()
    elif now.hour != 22:
        confirmed_today = False  # Réinitialise chaque jour
    time.sleep(60)
