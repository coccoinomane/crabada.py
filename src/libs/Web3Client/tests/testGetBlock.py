from src.common.config import nodeUri
from src.helpers.general import secondOrNone
from src.libs.Web3Client.Web3ClientFactory import makeWeb3Client
from src.libs.Web3Client.helpers.debug import pprintAttributeDict
from sys import argv

# VARS
client = makeWeb3Client("Avalanche", nodeUri)

# TEST FUNCTIONS
def test() -> None:
    print(">>> LATEST BLOCK")
    pprintAttributeDict(client.w3.eth.get_block("latest"))
    print(">>> PENDING BLOCK")
    pprintAttributeDict(client.w3.eth.get_block("pending"))


# EXECUTE
test()
