import requests
import os

# Telegram
TG_TOKEN = os.getenv("TG_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Telegraph
TELEGRAPH_TOKEN = os.getenv("TELEGRAPH_TOKEN")

# VK паблик
VK_DOMAIN = "fitness_technology"

# Получаем последний пост
vk_url = f"https://api.vk.com/method/wall.get?domain={VK_DOMAIN}&count=1&v=5.131"

response = requests.get(vk_url).json()

post = response["response"]["items"][0]

text = post.get("text", "Новый пост")

# Заголовок
title = text.split("\n")[0][:80]

# Создаем статью Telegraph
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

# Публикация в Telegram
telegram_url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"

message = f"""
🔥 {title}

Читать полностью:
{page_url}
"""

requests.post(telegram_url, data={
    "chat_id": CHAT_ID,
    "text": message
})

print("POSTED")