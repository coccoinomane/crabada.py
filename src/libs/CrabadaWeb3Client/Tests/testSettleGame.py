from sys import argv
from typing import cast
from src.libs.Web3Client.helpers.debug import printTxInfo
from src.common.config import nodeUri, users
from src.libs.CrabadaWeb3Client.CrabadaWeb3Client import CrabadaWeb3Client

# VARS
client = cast(
    CrabadaWeb3Client,
    (CrabadaWeb3Client().setNodeUri(nodeUri).setCredentials(users[0]["privateKey"])),
)

gameId = int(argv[1]) if len(argv) > 1 else 284549

# TEST FUNCTIONS
def testSettleGame() -> None:
    txHash = client.settleGame(gameId)
    printTxInfo(client, txHash)


# EXECUTE
testSettleGame()
