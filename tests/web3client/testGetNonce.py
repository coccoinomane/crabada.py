import sys
sys.path.insert(1, '../..')
from common.config import nodeUri, contract, users
from libs.crabada.web3client.Web3Client import Web3Client
from pprint import pprint

# VARS
client = (Web3Client()
    .setContractAddress(contract['address'])
    .setNodeUri(nodeUri)
    .setAbi(contract['abi'])
    .setCredentials(users[0]['address'], users[0]['privateKey'])
    .init())

# TEST FUNCTIONS
def testGetNonce():
    pprint(client.getNonce())

# EXECUTE
testGetNonce()