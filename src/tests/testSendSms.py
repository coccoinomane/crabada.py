"""Code from https://www.twilio.com/docs/sms/quickstart/python#install-python-and-the-twilio-helper-library"""

from src.helpers.sms import sendSms
from pprint import pprint

# VARS
body = "Join Earth's mightiest heroes. Like Kevin Bacon."

# TEST FUNCTIONS
def testSendSmsWithTwilio() -> None:
    output = sendSms(
        body=body,
        forceSend=True,  # send SMS regardless of settings
    )
    pprint(output)
    if output:
        pprint(vars(output))


# EXECUTE
testSendSmsWithTwilio()
