from sys import argv
from src.libs.CrabadaWeb2Client.MarketWeb2Client import MarketWeb2Client
from src.libs.CrabadaWeb2Client.types.marketTypes import SearchParameters
from src.libs.CrabadaWeb2Client.types.marketTypes import CrabClasses
from src.helpers.general import fourthOrNone, secondOrNone, thirdOrNone
from pprint import pprint

# VARS
client = MarketWeb2Client()
classNames: str = secondOrNone(argv)
pincersName: str = thirdOrNone(argv)
eyesName: str = fourthOrNone(argv)

params: SearchParameters = {
    "limit": 3000,
    "page": 1,
    "orderBy": "price",
    "order": "asc",
}

if classNames:
    params["class_ids[]"] = [
        CrabClasses[name.upper()].value for name in classNames.split(",")
    ]


# TEST FUNCTIONS
def test() -> None:
    crabs = client.listCrabsForSale(params=params)
    if pincersName:
        crabs = [c for c in crabs if c["pincers_name"].lower() == pincersName.lower()]
    if eyesName:
        crabs = [c for c in crabs if c["eyes_name"].lower() == eyesName.lower()]
    print(">>> FOUND CRABS")
    pprint(crabs)
    print(">>> SEARCH PARAMETERS")
    pprint(params)
    print(">>> N FOUND")
    pprint(len(crabs))


# EXECUTE
test()
