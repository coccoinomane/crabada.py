"""Helper functions to handle Crabada games"""

from typing import Any
from twilio.rest import Client
from src.common.config import twilio, notifications


def sendSms(body: str, forceSend: bool = False) -> dict[str, Any]:
    """Send an SMS to the number configured in .env; won't send
    anything if sms are disabled, unless forceSend is True"""

    if not notifications["sms"]["enable"] and not forceSend:
        return {}

    return sendTwilioSms(
        body=body,
        from_=str(notifications["sms"]["from"]),
        to=str(notifications["sms"]["to"]),
        accountSid=twilio["accountSid"],
        authToken=twilio["authToken"],
    )


def sendTwilioSms(
    body: str, from_: str, to: str, accountSid: str, authToken: str
) -> dict[str, Any]:
    """Send an SMS using Twilio"""
    client = Client(accountSid, authToken)
    return client.messages.create(
        body=body,
        from_=from_,
        to=to,
    )
