from src.libs.CrabadaWeb2Client.CrabadaWeb2Client import CrabadaWeb2Client
from pprint import pprint

# VARS
client = CrabadaWeb2Client()

# TEST FUNCTIONS
def testListCrabsForLendingByPrice() -> None:
    params = {"limit": 3, "page": 1, "orderBy": "price", "order": "asc"}
    pprint(client.listCrabsForLending(params=params))


def testListCrabsForLendingByMinePoints() -> None:
    params = {"limit": 3, "page": 1, "orderBy": "mine_point", "order": "desc"}
    pprint(client.listCrabsForLending(params=params))


# EXECUTE
print(">>> REINFORCEMENTS - CHEAPEST FIRST")
testListCrabsForLendingByPrice()
print(">>> REINFORCEMENTS - HIGHEST MINE POINTS FIRST")
testListCrabsForLendingByMinePoints()
