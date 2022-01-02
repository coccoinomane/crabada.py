from src.common.config import nodeUri, contract
from src.libs.Web3Client.Web3Client import Web3Client
from pprint import pprint

# VARS
client = (Web3Client()
    .setNodeUri(nodeUri)
    .setContract(contract['address'], contract['abi']))

# TEST FUNCTIONS
def testGetContract() -> None:
    print(">>> ABI")
    pprint(client.abi)
    print(">>> CONTRACT VARS")
    pprint(vars(client.contract))
    print(">>> CONTRACT FUNCTIONS")
    pprint(vars(client.contract.functions))

# EXECUTE
testGetContract()