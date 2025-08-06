# imports
import json
import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#BOT TOKEN to access it safely instead of hardcoding
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Chat ID to access it safely instead of hardcoding
CHAT_ID = os.environ.get("CHAT_ID")

# websites link that we use for scraping
FILTERED_URL = open("siteLink.txt", "r", encoding="utf-8").read()

#SPECIFIC_HOUSING_LINK_START = "https://plaza.newnewnew.space/"

# The time interval between every check
CHECK_INTERVAL = 5  # seconds

# The section that all of the housing ads are listed
DIV_HOUSING_SECTION = "section.list-item"

# The hash file that we save for each previous housing listings
HASH_FILE = "lasthash.json"

def load_last_hash():
    """
    Loads the last saved hash data from a JSON file.

    Returns:
        list: A list of hash entries loaded from HASH_FILE if it exists;
              otherwise, returns an empty list.

    Notes:
        - Expects `HASH_FILE` to be a valid file path (string) defined elsewhere.
        - The file should contain a JSON-encoded list.
    """
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, "r") as f:
            return json.load(f)
    return []

def save_last_hash(houses):
    """
    Saves the last fetched housing data to a JSON file.

    Args:
        houses (list): The list of housing adds that will be written to JSON file,
            as the style of dictionary.

    Notes:
        - If HASH_FILE does not exist, it will be created automatically.
        - The file content will be overwritten on each save.
    """
    with open(HASH_FILE, "w") as f:
        json.dump(houses, f)

def fetch_page_content(url):
    """_summary_

    Args:
        url (string): _description_

    Returns:
        BeautifulSoup or None: _description_
    """ 
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(options=options)
        driver.get(url)
        time.sleep(CHECK_INTERVAL)  # Wait for JavaScript to render
        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.quit()
    except Exception as e:
        print(f"Error fetching/parsing page: {e}")
        return None
    return soup

def parse_housing_data(soup):
    listings  = soup.select(DIV_HOUSING_SECTION)
    houses = []
    for listing in listings:
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
            "Link": link,
            "Price": price,
        })
    return houses

def adjust_message(house):
    output = "LUNA CIKTI ALOOOO \n"
    for name, info in house.items():
        if name == "Link":
            output += name + ": " + f'"https://plaza.newnewnew.space/{info}"\n'
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
    try:
        while True:
            LAST_HASH = load_last_hash()

            soup = fetch_page_content(FILTERED_URL)
            current_houses = parse_housing_data(soup)

            current_links = {h["Link"] for h in current_houses}
            last_links = {h["Link"] for h in LAST_HASH}

            new_links = current_links - last_links

            if new_links:
                save_last_hash(current_houses)
                for house in current_houses:
                    if house["Link"] in new_links:
                        msg  = adjust_message(house)
                        send_telegram_message(msg)
    except KeyboardInterrupt:
        print("Stopped by user")

if __name__ == "__main__":
    main()



