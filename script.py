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
CHECK_INTERVAL = 60  # seconds
LAST_HASH = None
DIV_HOUSING_SECTION = "section.list-item"


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
    listings  = soup.select(DIV_HOUSING_SECTION)
    houses = []
    for _, listing in enumerate(listings, 1):
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
            "Title": title,
            "Price": price,
            "Link": link, 
        })
    return houses

def adjust_message(houses):
    output = ""
    for house in houses:
        for name, info in house.items():
            if name == "Link":
                output += f"Link: [Click here]({info})\n"
            else:
                output += name + ": " + info + "\n"
    return output

def send_telegram_message(adjusted_message):
    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': adjusted_message,
        'parse_mode': 'Markdown'
    }
    try:
        requests.post(telegram_url, data=payload)
    except Exception as e:
        print(f"Error sending message: {e}")


def main():
    soup = fetch_page_content(FILTERED_URL)
    all_houses = parse_housing_data(soup)
    msg  = adjust_message(all_houses)
    send_telegram_message(msg)

if __name__ == "__main__":
    main()



