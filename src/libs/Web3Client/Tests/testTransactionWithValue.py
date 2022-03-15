from sys import argv
from typing import cast
from eth_typing import Address
from src.common.config import nodeUri, users
from src.libs.Web3Client.AvalancheCWeb3Client import AvalancheCWeb3Client
from src.libs.Web3Client.helpers.debug import printTxInfo
from pprint import pprint

# VARS
client = (
    AvalancheCWeb3Client()
    .setNodeUri(nodeUri)
    .setCredentials(users[0]["privateKey"])
    .setMaxPriorityFeePerGasInGwei(2)
)

to = cast(Address, "0xBc3a38C981B13625FAF7729fF105Cb6E15bdDE3A")
valueInEth = 0.00001  # ETH / AVAX / etc

# TEST FUNCTIONS
def testBuildTransactionWithValue() -> None:
    tx = client.buildTransactionWithValue(to, valueInEth)
    print(">>> TX")
    pprint(tx)


def testSignTransaction() -> None:
    tx = client.buildTransactionWithValue(to, valueInEth)
    signedTx = client.signTransaction(tx)
    print(">>> SIGNED TX")
    pprint(signedTx)


def testSendSignedTransaction() -> None:
    tx = client.buildTransactionWithValue(to, valueInEth)
    signedTx = client.signTransaction(tx)
    txHash = client.sendSignedTransaction(signedTx)
    printTxInfo(client, txHash)


# EXECUTE
testBuildTransactionWithValue()
testSignTransaction()
if len(argv) > 1 and argv[1] == "--send":
    testSendSignedTransaction()
