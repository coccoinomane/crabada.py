from typing import cast
from src.libs.Web3Client.helpers.debug import printTxInfo
from src.helpers.general import secondOrNone
from src.common.config import nodeUri, users, contract, chainId
from src.libs.CrabadaWeb3Client.CrabadaWeb3Client import CrabadaWeb3Client
from sys import argv

# VARS
client = cast(CrabadaWeb3Client, (CrabadaWeb3Client()
    .setNodeUri(nodeUri)
    .setContract(contract['address'], contract['abi'])
    .setCredentials(users[0]['address'], users[0]['privateKey'])
    .setChainId(chainId)))

teamId = users[0]['teams'][0]['id']
mineId = int(secondOrNone(argv))

# TEST FUNCTIONS
def testAttack() -> None:
    txHash = client.attack(mineId, teamId)
    printTxInfo(client, txHash)

# EXECUTE
testAttack()