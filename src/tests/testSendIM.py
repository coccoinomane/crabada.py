from sys import argv
from src.helpers.instantMessage import sendIM
from src.helpers.general import secondOrNone
from pprint import pprint

# VARS
silent = False if secondOrNone(argv) == "1" else True
body = "Join Earth's mightiest heroes. Like Kevin Bacon."

# TEST FUNCTIONS
def test() -> None:
    output = sendIM(
        body=body, forceSend=True, silent=silent  # send IM regardless of settings
    )
    print(">>> SILENT?")
    pprint(silent)
    print(">>> SUCCESS?")
    pprint(output)


# EXECUTE
test()
