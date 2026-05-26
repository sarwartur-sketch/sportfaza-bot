import requests
import os
import re

# Telegram
TG_TOKEN = os.getenv("TG_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Telegraph
TELEGRAPH_TOKEN = os.getenv("TELEGRAPH_TOKEN")

# VK страница
VK_URL = "https://vk.com/fitness_gym"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(VK_URL, headers=headers)

html = response.text

# Ищем текст поста
posts = re.findall(r'"text":"(.*?)"', html)

if not posts:
    raise Exception("Посты не найдены")

text = posts[0]

# Чистим текст
text = text.replace("\\n", "\n")
text = re.sub(r'<.*?>', '', text)

title = text.split("\n")[0][:80]

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

print(telegraph_response)

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