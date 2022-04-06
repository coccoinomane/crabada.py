from typing import cast
from eth_typing import Address
from src.common.config import nodeUri
from src.libs.Web3Client.AvalancheCErc20Web3Client import AvalancheCErc20Web3Client
from src.helpers.general import secondOrNone
from sys import argv

# VARS
tusTokenAddress = cast(Address, "0xf693248F96Fe03422FEa95aC0aFbBBc4a8FdD172")
tokenAddress = cast(Address, secondOrNone(argv) or tusTokenAddress)

client = AvalancheCErc20Web3Client(nodeUri=nodeUri, contractAddress=tokenAddress)

# TEST FUNCTIONS
def test() -> None:
    print(">>> TOKEN NAME")
    print(client.contract.functions.name().call())
    print(">>> TOKEN SYMBOL")
    print(client.contract.functions.symbol().call())
    print(">>> TOKEN TOTAL SUPPLY IN WEI")
    print(client.contract.functions.totalSupply().call())
    print(">>> TOKEN TOTAL SUPPLY IN ETHER")
    print(client.w3.fromWei(client.contract.functions.totalSupply().call(), "ether"))


# EXECUTE
test()
