import time
import requests
from datetime import datetime

BOT_TOKEN = 'TON_BOT_TOKEN'
CHAT_ID = 'ID_DE_TA_COPINE'
CONFIRMED = False
API_URL = f'https://api.telegram.org/bot{BOT_TOKEN}'

def send_reminder():
    reply_markup = {
        "inline_keyboard": [[
            {"text": "Confirmé ✅", "callback_data": "confirmed"}
        ]]
    }
    data = {
        "chat_id": CHAT_ID,
        "text": "Coucou mon amour 💖\nN'oublie pas de prendre ton médicament 💊\nClique sur le bouton quand c’est fait ✨",
        "reply_markup": reply_markup
    }
    requests.post(f"{API_URL}/sendMessage", json=data)

def check_confirmation(last_update_id):
    global CONFIRMED
    resp = requests.get(f"{API_URL}/getUpdates?offset={last_update_id + 1}").json()
    for update in resp.get("result", []):
        if "callback_query" in update:
            data = update["callback_query"]
            if data["data"] == "confirmed":
                CONFIRMED = True
                requests.post(f"{API_URL}/sendMessage", json={
                    "chat_id": CHAT_ID,
                    "text": "Bravo ma chérie 🎉 Tu as pris ton médicament ! 💖"
                })
        last_update_id = update["update_id"]
    return last_update_id

def main():
    print("Bot started")
    last_update_id = 0
    while True:
        now = datetime.now()
        if now.hour == 22 and now.minute == 0:
            send_reminder()
            while not CONFIRMED:
                time.sleep(600)  # Attendre 10 minutes
                if not CONFIRMED:
                    send_reminder()
                last_update_id = check_confirmation(last_update_id)
        time.sleep(30)

if __name__ == "__main__":
    main()
