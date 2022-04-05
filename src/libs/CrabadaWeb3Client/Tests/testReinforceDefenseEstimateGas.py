"""
Estimate the gas needed for a reinforceDefense transaction.

Will raise an "execution reverted" error if for any reason
the reinforce is not possible
"""

from typing import cast
from src.common.config import nodeUri, users
from src.libs.CrabadaWeb3Client.CrabadaWeb3Client import CrabadaWeb3Client
from src.libs.Web3Client.AvalancheCWeb3Client import AvalancheCWeb3Client
from pprint import pprint
from src.libs.Web3Client.helpers.debug import printTxInfo
from sys import argv
from web3.types import Wei

# VARS
contractAddress = CrabadaWeb3Client.contractAddress
contractAbi = CrabadaWeb3Client.abi

client = AvalancheCWeb3Client(
    nodeUri=nodeUri,
    contractAddress=contractAddress,
    abi=contractAbi,
    privateKey=users[0]["privateKey"],
)

# This set of parameters should return 210309
gameId = 3548809
crabadaId = 6817
borrowPrice = 17500000000000000000
blockWhenAvailable = 12973034
expectedGas = 210309

# Contract
teamId = users[0]["teams"][0]["id"]
contractFunction = client.contract.functions.reinforceDefense(
    gameId, crabadaId, borrowPrice
)
print(">>> FUNCTION")
pprint(contractFunction)
print(">>> ARGS")
pprint(contractFunction.arguments)
print(">>> ENCODED DATA")
pprint(contractFunction._encode_transaction_data())

# TEST FUNCTIONS
def test() -> None:
    baseTx = client.buildBaseTransaction()
    gas = contractFunction.estimateGas(baseTx, blockWhenAvailable)
    print(">>> ESTIMATE GAS")
    print(gas)
    assert gas == expectedGas


# EXECUTE
test()
