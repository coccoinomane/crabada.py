from libs.CrabadaWeb3Client.Tests.helpers import printTxInfo
from common.config import nodeUri, users, contract, chainId
from libs.CrabadaWeb3Client.CrabadaWeb3Client import CrabadaWeb3Client
from pprint import pprint

# VARS
client = (CrabadaWeb3Client()
    .setNodeUri(nodeUri)
    .setContract(contract['address'], contract['abi'])
    .setCredentials(users[0]['address'], users[0]['privateKey'])
    .setChainId(chainId))

# Contract
gameId = 284549

# TEST FUNCTIONS
def testCloseGame():
    txHash = client.closeGame(gameId)
    printTxInfo(client, txHash)

# EXECUTE
testCloseGame()