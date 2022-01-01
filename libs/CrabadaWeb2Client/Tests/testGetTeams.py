from common.config import users
from libs.CrabadaWeb2Client.CrabadaWeb2Client import CrabadaWeb2Client
from pprint import pprint

# VARS
client = CrabadaWeb2Client()
userAddress = users[0]['address']

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