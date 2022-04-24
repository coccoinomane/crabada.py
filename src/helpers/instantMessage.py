from src.common.config import notifications, telegram
from src.common.logger import logger
import requests
import json


def sendIM(body: str, forceSend: bool = False, silent: bool = True) -> bool:
    """
    Send an instant message to the services configured in .env;
    so far only Telegram is supported.

    Parameters
    ----------
    body : str
        The message to send; if the IM protocol supports it (Telegram does)
        it can include emojis.
    forceSend : bool
        Send the notification even if notifications are disabled
        at the config level.
    silent : bool
        Send a silent notification, if the IM protocol supports it
        (Telegram does)
    """

    if not notifications["instantMessage"]["enable"] and not forceSend:
        return True

    notification_result = False

    try:
        if telegram["enable"]:
            notification_result = sendTelegramMessage(
                body=body,
                apiKey=telegram["apiKey"],
                chatId=telegram["chatId"],
                disableNotifications=silent,
            )
        # NOTE <add more IM services here>

    except:
        logger.warning("Notification Error!")
        return False

    return notification_result


def sendTelegramMessage(
    body: str, apiKey: str, chatId: str, disableNotifications: bool = True
) -> bool:
    """
    Send a Telegram message using the REST api.

    Docs: https://core.telegram.org/bots/api#sendmessage
    """
    headers = {"Content-Type": "application/json"}

    data_dict = {
        "chat_id": chatId,
        "text": body,
        "parse_mode": "HTML",
        "disable_notification": disableNotifications,
    }
    data = json.dumps(data_dict)

    url = f"https://api.telegram.org/bot{apiKey}/sendMessage"
    response = requests.post(url, data=data, headers=headers, timeout=1)
    return response.ok
