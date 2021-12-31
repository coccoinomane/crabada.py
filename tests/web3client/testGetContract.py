import sys
sys.path.insert(1, '../..')
from common.config import nodeUri
from libs.crabada.web3client.Web3Client import Web3Client
from pprint import pprint

# VARS
client = Web3Client(nodeUri=nodeUri)

# TEST FUNCTIONS
def testGetContract():
    print(">>> CONTRACT VARS")
    pprint(vars(client.getContract()))
    print(">>> CONTRACT FUNCTIONS")
    pprint(vars(client.getContract().functions))

# EXECUTE
testGetContract()