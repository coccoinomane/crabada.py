import sys
sys.path.insert(1, '../..')
from common.config import nodeUri, users
from libs.crabada.web3client.Web3Client import Web3Client
from pprint import pprint

# VARS
client = Web3Client().setNodeUri(nodeUri)

# TEST FUNCTIONS
def testGetContract():
    userAddress = teams[0].userAddress
    userKey = [u for u in users if u.address == userAddress]
    
    output = client.startGame(usersteams[0].id)
    
    pprint(vars(client.getContract()))
    pprint(vars(client.getContract()))
    print(">>> CONTRACT FUNCTIONS")
    pprint(vars(client.getContract().functions))

# EXECUTE
testGetContract()