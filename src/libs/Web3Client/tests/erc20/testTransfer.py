from typing import cast
from eth_typing import Address
from src.common.config import nodeUri, users
from src.helpers.general import secondOrNone, thirdOrNone
from sys import argv
from src.libs.Web3Client.Erc20Web3Client import Erc20Web3Client
from src.libs.Web3Client.helpers.debug import printTxInfo
from src.libs.Web3Client.exceptions import Web3ClientException
from web3.exceptions import ContractLogicError

# VARS
tokenAddress = cast(Address, secondOrNone(argv) or "")
to = cast(Address, thirdOrNone(argv) or "")

if not tokenAddress:
    print("Please provide a token address")
    exit(1)

if not to:
    print("Please provide a recipient")
    exit(1)

amount = 1

client = Erc20Web3Client(
    nodeUri=nodeUri,
    contractAddress=tokenAddress,
    privateKey=users[0]["privateKey"],
    txType=2,
    chainId=43114,
)

# TEST FUNCTIONS
def test() -> None:
    txHash = client.transfer(to, amount)
    print(txHash)
    printTxInfo(client, txHash)


# EXECUTE
try:
    test()
except ContractLogicError as e:
    print(">>> CONTRACT EXCEPTION!")
    print(e)
except Web3ClientException as e:
    print(">>> CLIENT EXCEPTION!")
    print(e)
