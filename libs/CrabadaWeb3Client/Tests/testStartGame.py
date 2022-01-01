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
teamId = users[0]['teams'][0]['id']

# TEST FUNCTIONS
def testStartGame():
    txHash = client.startGame(teamId)
    printTxInfo(client, txHash)

# EXECUTE
testStartGame()