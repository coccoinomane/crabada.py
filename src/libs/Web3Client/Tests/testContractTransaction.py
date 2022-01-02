from src.common.config import nodeUri, users, contract, chainId
from src.libs.Web3Client.AvalancheWeb3Client import AvalancheWeb3Client
from pprint import pprint

# VARS
client = (AvalancheWeb3Client()
    .setNodeUri(nodeUri)
    .setContract(contract['address'], contract['abi'])
    .setCredentials(users[0]['address'], users[0]['privateKey'])
    .setChainId(chainId))

# Contract
teamId = users[0]['teams'][0]['id']
contractFunction = client.contract.functions.startGame(teamId)
pprint(contractFunction)

# TEST FUNCTIONS
def testBuildContractTransaction() -> None:
    pprint(client.buildContractTransaction(contractFunction))

# EXECUTE
testBuildContractTransaction()