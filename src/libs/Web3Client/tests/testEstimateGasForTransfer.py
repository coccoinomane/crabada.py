from sys import argv

from web3 import Web3
from src.common.config import nodeUri, users
from src.helpers.general import secondOrNone, thirdOrNone
from src.libs.Web3Client.AvalancheCWeb3Client import AvalancheCWeb3Client
from pprint import pprint

# VARS
client = AvalancheCWeb3Client(
    nodeUri=nodeUri,
    privateKey=users[0]["privateKey"],
)

to = secondOrNone(argv)
valueInEth = thirdOrNone(argv) or 1
valueInWei = Web3.toWei(valueInEth, "ether")

if not to:
    print("Provide a destination address")
    exit(1)

# TEST FUNCTIONS
def test() -> None:
    pprint(client.estimateGasForTransfer(to, valueInWei))


# EXECUTE
test()
