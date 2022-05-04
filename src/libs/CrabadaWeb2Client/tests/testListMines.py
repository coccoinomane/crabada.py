from src.common.config import users
from src.libs.CrabadaWeb2Client.CrabadaWeb2Client import CrabadaWeb2Client
from pprint import pprint

# VARS
client = CrabadaWeb2Client()
userAddress = users[0]["address"]

# TEST FUNCTIONS
def testGetOpenMines() -> None:
    params = {"limit": 3, "page": 1, "status": "open", "user_address": userAddress}
    pprint(client.listMines(params=params))


def testGetAllMines() -> None:
    params = {"limit": 3, "page": 1, "user_address": userAddress}
    pprint(client.listMines(params=params))


# EXECUTE
print(">>> OPEN MINES/GAMES")
testGetOpenMines()
print(">>> ALL MINES/GAMES (open and closed)")
testGetAllMines()
