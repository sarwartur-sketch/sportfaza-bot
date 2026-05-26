import requests
import os
import xml.etree.ElementTree as ET

# Telegram
TG_TOKEN = os.getenv("TG_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Telegraph
TELEGRAPH_TOKEN = os.getenv("TELEGRAPH_TOKEN")

# RSS VK
RSS_URL = "https://rss.app/feeds/v1.1/_R4XLK7Vw6eKxQz8m.xml"

# Получаем RSS
response = requests.get(RSS_URL)

root = ET.fromstring(response.content)

item = root.find("./channel/item")

title = item.find("title").text
description = item.find("description").text

text = f"{title}\n\n{description}"

# Telegraph
telegraph_url = "https://api.telegra.ph/createPage"

telegraph_data = {
    "access_token": TELEGRAPH_TOKEN,
    "title": title,
    "author_name": "SportFaza",
    "content": f'[{{"tag":"p","children":["{text}"]}}]',
    "return_content": False
}

telegraph_response = requests.post(
    telegraph_url,
    json=telegraph_data
).json()

page_url = telegraph_response["result"]["url"]

# Telegram
telegram_url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"

message = f"""
🔥 {title}

Читать полностью:
{page_url}
"""

telegram_response = requests.post(
    telegram_url,
    data={
        "chat_id": CHAT_ID,
        "text": message
    }
)

print(telegram_response.text)

print("POSTED")