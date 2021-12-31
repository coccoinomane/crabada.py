import sys
sys.path.insert(1, '../..')
from libs.crabada.web2client.Web2Client import Web2Client
from pprint import pprint

# VARS
client = Web2Client()
mineId = 269751

# TEST FUNCTIONS
def testGetMine():
    pprint(client.getMine(mineId).json())

# EXECUTE
testGetMine()