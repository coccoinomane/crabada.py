from src.common.config import users
from src.libs.CrabadaWeb2Client.IdleGameWeb2Client import IdleGameWeb2Client
from pprint import pprint

# VARS
client = IdleGameWeb2Client()
looterAddress = users[0]["address"]

# TEST FUNCTIONS
def test() -> None:
    pprint(client.listMyOpenLoots(looterAddress))


# EXECUTE
test()
