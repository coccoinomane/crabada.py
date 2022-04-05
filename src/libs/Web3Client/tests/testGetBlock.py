from src.common.config import nodeUri
from src.libs.Web3Client.AvalancheCWeb3Client import AvalancheCWeb3Client
from pprint import pprint

from src.libs.Web3Client.helpers.debug import pprintAttributeDict

# VARS
client = AvalancheCWeb3Client(nodeUri=nodeUri)

# TEST FUNCTIONS
def test() -> None:
    print(">>> LATEST BLOCK")
    pprintAttributeDict(client.w3.eth.get_block("latest"))
    print(">>> PENDING BLOCK")
    pprintAttributeDict(client.w3.eth.get_block("pending"))


# EXECUTE
test()
