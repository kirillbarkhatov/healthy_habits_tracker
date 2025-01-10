import requests
from config.settings import BOT_TOKEN

def send_telegram_message(chat_id, message):
    """Сервис для отправки напоминаний в телеграм"""

    params = {
        "text": message,
        "chat_id": chat_id,
    }

    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", params=params)
