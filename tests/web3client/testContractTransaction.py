import sys
sys.path.insert(1, '../..')
from common.config import nodeUri, users, contract, chainId
from libs.crabada.web3client.Web3Client import Web3Client
from pprint import pprint

# VARS
client = (Web3Client()
    .setNodeUri(nodeUri)
    .setContract(contract['address'], contract['abi'])
    .setCredentials(users[0]['address'], users[0]['privateKey'])
    .setChainId(chainId))

# Contract
teamId = users[0]['teams'][0]['id']
contractFunction = client.contract.functions.startGame(teamId)
pprint(contractFunction)

# TEST FUNCTIONS
def testBuildContractTransaction():
    pprint(client.buildContractTransaction(contractFunction))

# EXECUTE
testBuildContractTransaction()