from src.common.config import nodeUri, users
from src.libs.Web3Client.Web3Client import Web3Client
from pprint import pprint

# VARS
client = Web3Client().setNodeUri(nodeUri).setCredentials(users[0]["privateKey"])

# TEST FUNCTIONS
def testGetNonce() -> None:
    pprint(client.getNonce())


# EXECUTE
testGetNonce()
