import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


def send_telegram_message(chat_id, message):
    """Отправляет сообщение в Telegram через Bot API."""
    token = settings.TELEGRAM_BOT_TOKEN
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN не настроен")
        return None

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
    }
    try:
        response = requests.post(url, data=payload, timeout=10)
        response.raise_for_status()
        logger.info("Сообщение отправлено в чат %s", chat_id)
        return response
    except requests.RequestException as exc:
        logger.error("Ошибка отправки сообщения в Telegram: %s", exc)
        return None
