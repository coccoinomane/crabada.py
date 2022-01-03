"""Helper functions to handle Crabada games"""

from typing import Any
from twilio.rest import Client
from src.common.config import twilio

def sendSms(body: str) -> dict[str, Any]:
    """Send an SMS to the number configured in .env"""
    client = Client(twilio['accountSid'], twilio['authToken'])
    return client.messages.create(
        body = body,
        from_ = twilio['from'],
        to= twilio['to'],
    )