import requests, sys
sys.path.append("..")
from Client import Client
from pprint import pprint

# VARS
client = Client()
userAddress = "0x5818a5f1Ff6df3B7f5daD8Ac66E100CCe9E33E8e"

# TEST FUNCTIONS
def testGetAvailableTeams():
    params = {"limit": 5, "page": 1, "is_team_available": 1}
    pprint(client.getTeams(userAddress, params=params).json())

def testGetAllTeams():
    pprint(client.getTeams(userAddress).json())

# EXECUTE
print(">>> AVAILABLE TEAMS")
testGetAvailableTeams()
print(">>> ALL TEAMS")
testGetAllTeams()