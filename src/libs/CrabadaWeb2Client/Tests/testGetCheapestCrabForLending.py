from src.libs.CrabadaWeb2Client.CrabadaWeb2Client import CrabadaWeb2Client
from pprint import pprint

from src.libs.CrabadaWeb2Client.types import CrabForLending

# VARS
client = CrabadaWeb2Client()

# TEST FUNCTIONS
def test() -> None:
    pprint(client.getCheapestCrabForLending())


# EXECUTE
test()
