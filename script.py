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
FILTERED_URL = "https://plaza.newnewnew.space/en/availables-places/living-place#?gesorteerd-op=publicatiedatum-&locatie=Eindhoven-Nederland%2B-%2BNoord-Brabant"
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
        time.sleep(2)  # Wait for JavaScript to render
        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.quit()
    except Exception as e:
        print(f"Error fetching/parsing page: {e}")
        return None 
    return soup

def parse_housing_data(soup):
    listings  = soup.select("section.list-item")
    houses = []
    for idx, listing in enumerate(listings, 1):
        # Link to listing
        link_tag = listing.select_one("a[href]")
        #print(link_tag)
        link = link_tag["href"] if link_tag else None

        alternative_name_index  = link_tag["href"].find("details/")

        # Name of the Listing
        img_tag = listing.select_one("img[alt]")
        #print(img_tag)
        title = img_tag["alt"] if img_tag and img_tag.has_attr("alt") else (
            link_tag["href"][alternative_name_index:] if link_tag else "No title found"
        )

        # Price
        price_tag = listing.select_one("span.prijs.ng-binding.ng-scope")
        price = price_tag.get_text(strip=True) if price_tag else "No price found"

        houses.append({
            "title": title,
            "link": link,
            "price": price,
        })

        print(f"Listing #{idx}")
        print(f"Title: {title}")
        print(f"Link: {link}")
        print(f"Price: {price}")
        print("-" * 40)


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



