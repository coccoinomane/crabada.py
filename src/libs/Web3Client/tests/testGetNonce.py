from src.common.config import nodeUri, users
from src.libs.Web3Client.Web3Client import Web3Client
from pprint import pprint

# VARS
client = Web3Client(
    nodeUri=nodeUri,
    privateKey=users[0]["privateKey"],
)

# TEST FUNCTIONS
def test() -> None:
    pprint(client.getNonce())


# EXECUTE
test()
