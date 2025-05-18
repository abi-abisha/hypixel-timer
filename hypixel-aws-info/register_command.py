import requests

BOT_TOKEN = ''
APP_ID = ''

url = f"https://discord.com/api/v10/applications/{APP_ID}/commands"

payload = {
    "name": "timetable",
    "description": "Display this week’s activity.",
    "type": 1  # 1 = CHAT_INPUT (slash command)
}

headers = {
    "Authorization": f"Bot {BOT_TOKEN}",
    "Content-Type": "application/json"
}

# r = requests.post(url, json=payload, headers=headers)
r = requests.get(url, headers=headers)
print(r.status_code, r.text)
