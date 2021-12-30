import requests, sys
sys.path.append("..")
from Client import Client
from pprint import pprint

# VARS
client = Client()
mineId = 269751

# TEST FUNCTIONS
def testGetMine():
    pprint(client.getMine(mineId).json())

# EXECUTE
testGetMine()