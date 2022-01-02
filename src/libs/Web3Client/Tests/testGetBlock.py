from src.common.config import nodeUri, users
from src.libs.Web3Client.AvalancheWeb3Client import AvalancheWeb3Client
from pprint import pprint

# VARS
client = (AvalancheWeb3Client()
    .setNodeUri(nodeUri)
    .setCredentials(users[0]['address'], users[0]['privateKey']))

# TEST FUNCTIONS
def testGetBlock() -> None:
    print('>>> LATEST BLOCK')
    pprint(client.w3.eth.get_block('latest'))
    print('>>> PENDING BLOCK')
    pprint(client.w3.eth.get_block('pending'))

# EXECUTE
testGetBlock()