from src.common.config import nodeUri, users
from src.libs.CrabadaWeb3Client.CrabadaWeb3Client import CrabadaWeb3Client
from src.libs.Web3Client.AvalancheCWeb3Client import AvalancheCWeb3Client
from pprint import pprint
from src.libs.Web3Client.helpers.debug import printTxInfo
from sys import argv

# VARS
contractAddress = CrabadaWeb3Client.contractAddress
contractAbi = CrabadaWeb3Client.abi

client = (
    AvalancheCWeb3Client()
    .setNodeUri(nodeUri)
    .setContract(address=contractAddress, abi=contractAbi)
    .setCredentials(users[0]["privateKey"])
)

# Contract
teamId = users[0]["teams"][0]["id"]
contractFunction = client.contract.functions.startGame(teamId)
pprint(contractFunction)

# TEST FUNCTIONS
def testBuildContractTransaction() -> None:
    pprint(client.buildContractTransaction(contractFunction))


def testSendContractTransaction() -> None:
    tx = client.buildContractTransaction(contractFunction)
    txHash = client.signAndSendTransaction(tx)
    printTxInfo(client, txHash)


# EXECUTE
testBuildContractTransaction()
if len(argv) > 1 and argv[1] == "--send":
    testSendContractTransaction()
