import sys
sys.path.insert(1, '../..')
from common.config import nodeUri, contract
from libs.crabada.web3client.Web3Client import Web3Client
from pprint import pprint

# VARS
client = Web3Client().setContractAddress(contract['address']).setNodeUri(nodeUri).setAbi(contract['abi'])

# TEST FUNCTIONS
def testGetAbi():
    pprint(client.abi)

# EXECUTE
testGetAbi()