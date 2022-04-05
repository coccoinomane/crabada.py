from sys import argv
from typing import cast
from src.helpers.general import secondOrNone
from src.libs.Web3Client.helpers.debug import printTxInfo
from src.common.config import nodeUri, users
from src.libs.CrabadaWeb3Client.CrabadaWeb3Client import CrabadaWeb3Client
from web3.exceptions import ContractLogicError

# VARS
client = CrabadaWeb3Client(nodeUri=nodeUri, privateKey=users[0]["privateKey"])

gameId = int(secondOrNone(argv) or 284549)

# TEST FUNCTIONS
def test() -> None:
    txHash = client.closeGame(gameId)
    printTxInfo(client, txHash)


# EXECUTE
try:
    test()
except ContractLogicError as e:
    print(">>> CONTRACT EXCEPTION!")
    print(e)
