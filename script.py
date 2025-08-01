import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
import os
import time

BOT_TOKEN = ""
CHAT_ID = ""
FILTERED_URL = "https://plaza.newnewnew.space/en/availables-places/living-place#?gesorteerd-op=prijs%2B&locatie=Eindhoven-Nederland%2B-%2BNoord-Brabant"
HOUSING_URL = "https://plaza.newnewnew.space/en/availables-places/living-place/details/"
CHECK_INTERVAL = 60  # seconds
LAST_HASH = None
DIV_CLASS = 'ng-scope object-list-items-container'


def fetch_page_content(url):
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(options=options)
        driver.get(url)
        time.sleep(5)  # Wait for JavaScript to render
        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.quit()
    except Exception as e:
        print(f"Error fetching/parsing page: {e}")
        return None
    return soup

def parse_housing_data(soup):
    houses  = soup.select("section.list-item")
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


def main():
    #send_telegram_message()
    soup = fetch_page_content(FILTERED_URL)
    parse_housing_data(soup)

if __name__ == "__main__":
    main()



