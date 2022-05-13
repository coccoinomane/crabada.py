from sys import argv
from typing import cast
from eth_typing import Address
from src.common.config import nodeUri, users
from src.libs.Web3Client.SwimmerNetworkWeb3Client import SwimmerNetworkWeb3Client
from src.libs.Web3Client.helpers.debug import printTxInfo
from pprint import pprint

# VARS
client = SwimmerNetworkWeb3Client(
    nodeUri=nodeUri,
    privateKey=users[0]["privateKey"],
)

to = cast(Address, "0xb697fAC04e7c16f164ff64355D5dCd9247aC5434")
valueInEth = 0.000000001  # ETH / AVAX / etc

# TEST FUNCTIONS
def testBuild() -> None:
    tx = client.buildTransactionWithValue(to, valueInEth)
    print(">>> TX")
    pprint(tx)


def testSign() -> None:
    tx = client.buildTransactionWithValue(to, valueInEth)
    signedTx = client.signTransaction(tx)
    print(">>> SIGNED TX")
    pprint(signedTx)


def testSend() -> None:
    txHash = client.sendEth(to, valueInEth)
    printTxInfo(client, txHash)


# EXECUTE
testBuild()
testSign()
if len(argv) > 1 and argv[1] == "--send":
    testSend()
