from src.libs.CrabadaWeb2Client.IdleGameWeb2Client import IdleGameWeb2Client
from pprint import pprint


# VARS
client = IdleGameWeb2Client()

# TEST FUNCTIONS
def test() -> None:
    pprint(client.getCheapestCrabForLending())


# EXECUTE
test()
