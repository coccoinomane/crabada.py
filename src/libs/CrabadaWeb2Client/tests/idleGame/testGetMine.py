from src.helpers.general import secondOrNone
from src.libs.CrabadaWeb2Client.IdleGameWeb2Client import IdleGameWeb2Client
from pprint import pprint
from sys import argv

# VARS
client = IdleGameWeb2Client()
mineId = secondOrNone(argv) or 269751

# TEST FUNCTIONS
def test() -> None:
    pprint(client.getMine(mineId))


# EXECUTE
test()
