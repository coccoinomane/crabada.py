from sys import argv
from src.libs.CrabadaWeb2Client.MarketWeb2Client import MarketWeb2Client
from src.libs.CrabadaWeb2Client.types.marketTypes import SearchParameters
from src.libs.CrabadaWeb2Client.types.marketTypes import CrabClasses
from src.helpers.general import secondOrNone
from pprint import pprint

# VARS
client = MarketWeb2Client()
classNames = secondOrNone(argv)

params: SearchParameters = {
    "limit": 3,
    "page": 1,
}

if classNames:
    params["class_ids[]"] = [
        CrabClasses[name.upper()].value for name in classNames.split(",")
    ]


# TEST FUNCTIONS
def test() -> None:
    pprint(client.listCrabsForSale(params=params))


# EXECUTE
print(">>> SEARCH PARAMETERS")
pprint(params)
test()
