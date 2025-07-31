import requests
from bs4 import BeautifulSoup

BOT_TOKEN = "7826512571:AAGDi2IP_K0ccQLMKLGkxQZzW8iYDIa-GAM"
CHAT_ID = "7501622399"
FILTERED_URL = "https://plaza.newnewnew.space/en/availables-places/living-place#?gesorteerd-op=prijs%2B&locatie=Eindhoven-Nederland%2B-%2BNoord-Brabant"
HOUSING_URL = "https://plaza.newnewnew.space/en/availables-places/living-place/details/"
CHECK_INTERVAL = 60  # seconds
LAST_HASH = None
DIV_CLASS = 'ng-scope object-list-items-container'


def fetch_page_content(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        print(soup.prettify())  # Print the HTML content for debugging
    except Exception as e:
        print(f"Error fetching/parsing page: {e}")
        return None
    return soup

def parse_housing_data(soup):
    houses = soup.select(DIV_CLASS)
    print(houses)  # Print the housing data for debugging



def send_telegram_message():
    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': FILTERED_URL
    }
    try:
        requests.post(telegram_url, data=payload)
    except Exception as e:
        print(f"Error sending message: {e}")


#send_telegram_message()
soup = fetch_page_content(FILTERED_URL)
parse_housing_data(soup)

