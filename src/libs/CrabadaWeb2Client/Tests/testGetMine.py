from src.helpers.general import secondOrNone
from src.libs.CrabadaWeb2Client.CrabadaWeb2Client import CrabadaWeb2Client
from pprint import pprint
from sys import argv

# VARS
client = CrabadaWeb2Client()
mineId = secondOrNone(argv) or 269751

# TEST FUNCTIONS
def testGetMine() -> None:
    pprint(client.getMine(mineId))


# EXECUTE
testGetMine()
