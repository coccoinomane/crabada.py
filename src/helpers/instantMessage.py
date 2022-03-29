from src.common.config import notifications, telegram
from src.common.logger import logger

import requests
import json


def sendIM(body: str, forceSend: bool = False) -> bool:
    """Send an notification message to the service configured in .env; won't send
    anything if notifications are disabled, unless forceSend is True"""

    if not notifications["instantMessage"]["enable"] and not forceSend:
        return True

    notification_result = False
    try:
        if telegram["enable"]:
            notification_result = sendTelegramMessage(
                body=body, apiKey=telegram["apiKey"], chatId=telegram["chatId"]
            )

        # NOTE <add more IM services here>

    except:
        logger.warning("Notification Error!")
        return False

    return notification_result


def sendTelegramMessage(body: str, apiKey: str, chatId: str) -> bool:
    """Send a telegram message using rest api"""
    headers = {"Content-Type": "application/json"}

    data_dict = {
        "chat_id": chatId,
        "text": body,
        "parse_mode": "HTML",
        "disable_notification": True,
    }
    data = json.dumps(data_dict)

    url = f"https://api.telegram.org/bot{apiKey}/sendMessage"
    response = requests.post(url, data=data, headers=headers, timeout=1)
    return response.ok
