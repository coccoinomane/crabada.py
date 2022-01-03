"""Code from https://www.twilio.com/docs/sms/quickstart/python#install-python-and-the-twilio-helper-library"""

from twilio.rest import Client
from src.common.config import twilio
from pprint import pprint

# VARS
client = Client(twilio['accountSid'], twilio['authToken'])
body = "Join Earth's mightiest heroes. Like Kevin Bacon."
from_ = twilio['from']
to = twilio['to']

# TEST FUNCTIONS
def testSendSmsWithTwilio() -> None:
    output = client.messages.create(
        body = body,
        from_ = from_,
        to= to,
    )
    pprint(output)
    pprint(vars(output))

# EXECUTE
testSendSmsWithTwilio()