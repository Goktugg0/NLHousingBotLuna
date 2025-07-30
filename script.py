import requests
from bs4 import BeautifulSoup

BOT_TOKEN = ""
CHAT_ID = ""
FILTERED_URL = "https://plaza.newnewnew.space/en/availables-places/living-place#?gesorteerd-op=prijs%2B&locatie=Eindhoven-Nederland%2B-%2BNoord-Brabant"
CHECK_INTERVAL = 60  # seconds
LAST_HASH = None


def fetch_page_content(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        print(soup.prettify())  # Print the HTML content for debugging
    except Exception as e:
        print(f"Error fetching/parsing page: {e}")

def send_telegram_message():
    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': "HI"
    }
    try:
        requests.post(telegram_url, data=payload)
    except Exception as e:
        print(f"Error sending message: {e}")
send_telegram_message()
fetch_page_content(FILTERED_URL)

