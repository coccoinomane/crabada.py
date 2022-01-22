from src.common.config import nodeUri, users
from src.libs.Web3Client.AvalancheCWeb3Client import AvalancheCWeb3Client
from pprint import pprint

from src.libs.Web3Client.helpers.debug import pprintAttributeDict

# VARS
client = (AvalancheCWeb3Client()
    .setNodeUri(nodeUri)
    .setCredentials(users[0]['address'], users[0]['privateKey']))

# TEST FUNCTIONS
def testGetBlock() -> None:
    print('>>> LATEST BLOCK')
    pprintAttributeDict(client.w3.eth.get_block('latest'))
    print('>>> PENDING BLOCK')
    pprintAttributeDict(client.w3.eth.get_block('pending'))

# EXECUTE
testGetBlock()