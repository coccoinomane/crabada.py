from src.common.config import users
from src.libs.CrabadaWeb2Client.CrabadaWeb2Client import CrabadaWeb2Client
from pprint import pprint

# VARS
client = CrabadaWeb2Client()
looterAddress = users[0]["address"]

# TEST FUNCTIONS
def testListMyOpenLoots() -> None:
    pprint(client.listMyOpenLoots(looterAddress))


# EXECUTE
testListMyOpenLoots()
