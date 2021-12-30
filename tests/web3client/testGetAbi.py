import sys
sys.path.insert(1, '../..')
import common
from libs.crabada.web3client.Web3Client import Web3Client
from pprint import pprint

# VARS
client = Web3Client(nodeUri=common.getenv('WEB3_NODE_URI'))

# TEST FUNCTIONS
def testGetAbi():
    pprint(client.getAbi())

# EXECUTE
testGetAbi()