"""Code from https://www.twilio.com/docs/sms/quickstart/python#install-python-and-the-twilio-helper-library"""

from src.helpers.instant_message import sendIM
from pprint import pprint

# VARS
body = "Join Earth's mightiest heroes. Like Kevin Bacon."

# TEST FUNCTIONS
def test() -> None:
    output = sendIM(
        body=body,
        forceSend=True,  # send IM regardless of settings
    )
    print(">>> SUCCESS?")
    pprint(output)


# EXECUTE
test()
