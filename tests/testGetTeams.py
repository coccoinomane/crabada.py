import sys
sys.path.insert(1, '..')
import common
from libs.crabada.web2client.Web2Client import Web2Client
from pprint import pprint

# VARS
client = Web2Client()
userAddress = common.getenv('USER_ADDRESS')

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