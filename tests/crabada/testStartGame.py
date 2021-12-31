import sys
sys.path.insert(1, '../..')
from tests.helpers.transactions import printTxInfo
from common.config import nodeUri, users, contract, chainId
from libs.crabada.web3client.CrabadaWeb3Client import CrabadaWeb3Client
from pprint import pprint

# VARS
client = (CrabadaWeb3Client()
    .setContractAddress(contract['address'])
    .setNodeUri(nodeUri)
    .setAbi(contract['abi'])
    .setCredentials(users[0]['address'], users[0]['privateKey'])
    .setChainId(chainId)
    .init())

# Gas
gas = 300000 # units
gasPrice = 50 # gwei

# Contract
teamId = users[0]['teams'][0]['id']

# TEST FUNCTIONS
def testStartGame():
    txHash = client.startGame(teamId, gas, gasPrice)
    printTxInfo(client, txHash)

# EXECUTE
testStartGame()