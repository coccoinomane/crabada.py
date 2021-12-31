import sys
sys.path.insert(1, '../..')
from common.config import nodeUri, users, contract, chainId
from libs.crabada.web3client.Web3Client import Web3Client
from pprint import pprint

# VARS
client = (Web3Client()
    .setContractAddress(contract['address'])
    .setNodeUri(nodeUri)
    .setAbi(contract['abi'])
    .setCredentials(users[0]['address'], users[0]['privateKey'])
    .setChainId(chainId)
    .init())

# Gas
gas = 200000 # units
gasPrice = 25 # gwei

# Contract
teamId = users[0]['teams'][0]['id']
contractFunction = client.contract.functions.startGame(teamId)
pprint(contractFunction)

# TEST FUNCTIONS
def testBuildContractTransaction():
    pprint(client.buildContractTransaction(contractFunction, gas, gasPrice))

# EXECUTE
testBuildContractTransaction()