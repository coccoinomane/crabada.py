from src.common.config import nodeUri
from src.libs.Web3Client.Web3Client import Web3Client
from src.libs.CrabadaWeb3Client.CrabadaWeb3Client import CrabadaWeb3Client
from pprint import pprint

# VARS
contractAddress = CrabadaWeb3Client.contractAddress
contractAbi = CrabadaWeb3Client.abi

client = (
    Web3Client()
    .setNodeUri(nodeUri)
    .setContract(address=contractAddress, abi=contractAbi)
)

# TEST FUNCTIONS
def testGetContract() -> None:
    print(">>> CHECKSUM ADDRESS")
    print(">>> " + client.contractChecksumAddress)
    print(">>> ABI")
    pprint(client.abi)
    print(">>> CONTRACT VARS")
    pprint(vars(client.contract))
    print(">>> CONTRACT FUNCTIONS")
    pprint(vars(client.contract.functions))


# EXECUTE
testGetContract()
