from typing import cast
from src.libs.Web3Client.helpers.debug import printTxInfo
from src.common.config import nodeUri, users
from src.libs.CrabadaWeb3Client.CrabadaWeb3Client import CrabadaWeb3Client
from web3.exceptions import ContractLogicError

# VARS
client = CrabadaWeb3Client(nodeUri=nodeUri, privateKey=users[0]["privateKey"])

teamId = users[0]["teams"][0]["id"]

# TEST FUNCTIONS
def testStartGame() -> None:
    txHash = client.startGame(teamId)
    printTxInfo(client, txHash)


# EXECUTE
try:
    testStartGame()
except ContractLogicError as e:
    print(">>> CONTRACT EXCEPTION!")
    print(e)
