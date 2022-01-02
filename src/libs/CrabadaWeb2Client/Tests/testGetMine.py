from src.libs.CrabadaWeb2Client.CrabadaWeb2Client import CrabadaWeb2Client
from pprint import pprint

# VARS
client = CrabadaWeb2Client()
mineId = 269751

# TEST FUNCTIONS
def testGetMine() -> None:
    pprint(client.getMine(mineId).json())

# EXECUTE
testGetMine()