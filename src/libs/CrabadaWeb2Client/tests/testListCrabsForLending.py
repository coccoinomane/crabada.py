from src.libs.CrabadaWeb2Client.IdleGameWeb2Client import IdleGameWeb2Client
from pprint import pprint

# VARS
client = IdleGameWeb2Client()

# TEST FUNCTIONS
def testByPrice() -> None:
    params = {"limit": 3, "page": 1, "orderBy": "price", "order": "asc"}
    pprint(client.listCrabsForLending(params=params))


def testByMp() -> None:
    params = {"limit": 3, "page": 1, "orderBy": "mine_point", "order": "desc"}
    pprint(client.listCrabsForLending(params=params))


# EXECUTE
print(">>> REINFORCEMENTS - CHEAPEST FIRST")
testByPrice()
print(">>> REINFORCEMENTS - HIGHEST MINE POINTS FIRST")
testByMp()
