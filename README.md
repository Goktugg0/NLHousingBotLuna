# NLHousingBotLuna
A Python script that automatically monitors a housing listings on NewnewPlaza for new properties and sends notifications via a TelegramBot when there is a new house listing.

## Features

- Fetches housing listings from a given URL (see siteLink.txt).
- Uses Selenium (headless Chrome) to load and parse dynamic content.
- Detects only **newly added** listings.
- Sends notifications to Telegram via bot.
- Saves the last fetched listings to avoid spamming.

## Requirements
- Python 3.8+
- Google Chrome browser
- ChromeDriver (matching your Chrome version)
- Telegram bot token & chat ID
- The following Python packages:
  - `requests`
  - `beautifulsoup4`
  - `selenium`

