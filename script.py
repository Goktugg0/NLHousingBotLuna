import requests

BOT_TOKEN = ""
CHAT_ID = ""
URL = "./siteLink.txt"
CHECK_INTERVAL = 60  # seconds
LAST_HASH = None

def send_telegram_message():
    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': "HI"
    }
    requests.post(telegram_url, data=payload)
send_telegram_message()

