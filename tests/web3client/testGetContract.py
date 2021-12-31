import sys
sys.path.insert(1, '../..')
from common.config import nodeUri, contract
from libs.crabada.web3client.Web3Client import Web3Client
from pprint import pprint

# VARS
client = Web3Client().setContractAddress(contract['address']).setNodeUri(nodeUri).setAbi(contract['abi']).init()

# TEST FUNCTIONS
def testGetContract():
    print(">>> CONTRACT VARS")
    pprint(vars(client.contract))
    print(">>> CONTRACT FUNCTIONS")
    pprint(vars(client.contract.functions))

# EXECUTE
testGetContract()