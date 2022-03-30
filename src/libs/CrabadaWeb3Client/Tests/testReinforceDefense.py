from typing import cast
from src.helpers.reinforce import minerCanReinforce
from src.libs.Web3Client.helpers.debug import printTxInfo
from src.common.config import nodeUri, users
from src.libs.CrabadaWeb3Client.CrabadaWeb3Client import CrabadaWeb3Client
from src.libs.CrabadaWeb2Client.CrabadaWeb2Client import CrabadaWeb2Client
from web3 import Web3
from pprint import pprint
from src.models.User import User

# VARS
web3Client = cast(
    CrabadaWeb3Client,
    (CrabadaWeb3Client().setNodeUri(nodeUri).setCredentials(users[0]["privateKey"])),
)

web2Client = CrabadaWeb2Client()

userAddress = users[0]["address"]

openMines = web2Client.listMyOpenMines(userAddress)
if not openMines:
    print(f"User {str(userAddress)} has no open mines")
    exit(1)

cheapestCrab = web2Client.getCheapestCrabForLending()
if not cheapestCrab:
    print(f"Could not find a crab to lend")
    exit(1)

price = cheapestCrab["price"]
if User(userAddress).isTooExpensiveToBorrowTusWei(price):
    print(
        f"Price of crab is {Web3.fromWei(price, 'ether')} TUS which exceeds the user limit of {Web3.fromWei(users[0]['reinforcementMaxPriceInTusWei'], 'ether')}"
    )
    exit(1)

# TEST FUNCTIONS
def printGameInfo() -> None:
    print(">>> MINE")
    pprint(openMines[0])
    print(">>> REINFORCEMENT")
    pprint(cheapestCrab)
    print(">>> PRICE IN TUS")
    pprint(Web3.fromWei(price, "ether"))


def testReinforceDefense() -> None:
    txHash = web3Client.reinforceDefense(
        openMines[0]["game_id"], cheapestCrab["crabada_id"], cheapestCrab["price"]
    )
    printTxInfo(web3Client, txHash)


# EXECUTE
printGameInfo()

if not minerCanReinforce(openMines[0]):
    print(f"Miner cannot reinforce right now")
    exit(0)

testReinforceDefense()
