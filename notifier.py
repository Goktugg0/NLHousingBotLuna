# Imports
import json
import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Environment variables (for security)
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

# Constants
CHECK_INTERVAL = 5  # seconds between each page check
HOUSING_SECTION = "section.list-item" # The section that contains all of the houses
HASH_FILE = "lasthash.json" # The hash file to be written

# Load URL from file allowing variability
with open("siteLink.txt", "r", encoding="utf-8") as f:
    SITE_URL_WITH_FILTER = f.read()

def load_last_hash():
    """
    Load the last saved hash data from a JSON file.
    Return empty if doesn't exists.
    """
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, "r") as f:
            return json.load(f)
    return []

def save_last_hash(houses):
    """Save the latest housing data to a JSON file."""
    with open(HASH_FILE, "w") as f:
        json.dump(houses, f)

def fetch_page_content(url):
    """Fetch and parse HTML content from a webpage using a headless browser."""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        time.sleep(CHECK_INTERVAL)  # Allow time for JS to render
        soup = BeautifulSoup(driver.page_source, "html.parser") # Parse the website
    except Exception as e:
        print(f"Error fetching/parsing page: {e}")
        return None
    finally:
        driver.quit() # Quits the driver in any case

    return soup

def parse_housing_data(soup):
    """Extract housing listings from parsed HTML."""
    listings = soup.select(HOUSING_SECTION) # Selects the houses with CSS selector.
    houses = []

    for listing in listings:
        # Getting the link of the website
        link_tag = listing.select_one("a[href]")
        link = link_tag["href"] if link_tag else None

        alternative_name_index  = link_tag["href"].find("details/")

        # Extract the name of the listing
        img_tag = listing.select_one("img[alt]")
        # If no title is found get the data from the link and put it as name
        title = img_tag["alt"] if img_tag and img_tag.has_attr("alt") else (
            link_tag["href"][alternative_name_index:] if link_tag else "No title found"
        )

        # Extract Price
        price_tag = listing.select_one("span.prijs.ng-binding.ng-scope")
        price = price_tag.get_text(strip=True) if price_tag else "No price found"

        # Add to the array as dictionary for each house.
        houses.append({
            "Title": title,
            "Link": link,
            "Price": price,
        })
    return houses

def adjust_message(house):
    """It prettifies the message that will be sent via bot."""
    output = "A new housing is added! \n"
    for name, info in house.items():
        if name == "Link":
            output += name + ": " + f'"https://plaza.newnewnew.space/{info}"\n'
        else:
            output += name + ": " + info + "\n"
    return output

def send_telegram_message(adjusted_message):
    """Receive the prettified message and sends it to the user with library requests."""
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
    """Main loop to check for new listings and send messages via Telegram Bot."""
    try:
        while True:
            last_hash = load_last_hash()

            soup = fetch_page_content(SITE_URL_WITH_FILTER)
            if not soup:
                print("Failed to fetch page content.")
                time.sleep(CHECK_INTERVAL)
                continue

            current_houses = parse_housing_data(soup)

            current_links = {h["Link"] for h in current_houses}
            last_links = {h["Link"] for h in last_hash}

            new_links = current_links - last_links # Finds only the new links

            if new_links: # No messages if a housing is removed
                save_last_hash(current_houses)
                for house in current_houses:
                    if house["Link"] in new_links:
                        message  = adjust_message(house)
                        send_telegram_message(message)

            time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:
        print("Stopped by user")

if __name__ == "__main__":
    main()



