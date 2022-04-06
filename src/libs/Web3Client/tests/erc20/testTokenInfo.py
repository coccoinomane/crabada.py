from typing import cast
from eth_typing import Address
from src.common.config import nodeUri
from src.libs.Web3Client.Erc20Web3Client import Erc20Web3Client
from src.helpers.general import secondOrNone
from sys import argv

# VARS
tusTokenAddress = cast(Address, "0xf693248F96Fe03422FEa95aC0aFbBBc4a8FdD172")
tokenAddress = cast(Address, secondOrNone(argv) or tusTokenAddress)

client = Erc20Web3Client(
    nodeUri=nodeUri, contractAddress=tokenAddress, txType=2, chainId=43114
)

# TEST FUNCTIONS
def test() -> None:
    print(">>> TOKEN NAME")
    print(client.name())
    print(">>> TOKEN SYMBOL")
    print(client.symbol())
    print(">>> TOKEN DECIMALS")
    print(client.decimals())
    print(">>> TOKEN TOTAL SUPPLY IN WEI")
    print(client.totalSupply())
    print(">>> TOKEN TOTAL SUPPLY IN ETHER")
    print(client.w3.fromWei(client.totalSupply(), "ether"))


# EXECUTE
test()
