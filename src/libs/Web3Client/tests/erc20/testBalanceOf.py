from typing import cast
from eth_typing import Address
from src.common.config import nodeUri, users
from src.helpers.general import secondOrNone
from sys import argv
from src.libs.Web3Client.Web3ClientFactory import (
    makeErc20Client,
)

# VARS
tusTokenAddress = cast(Address, "0xf693248F96Fe03422FEa95aC0aFbBBc4a8FdD172")
tokenAddress = cast(Address, secondOrNone(argv) or tusTokenAddress)

client = makeErc20Client("Avalanche", nodeUri, tokenAddress)

# TEST FUNCTIONS
def test() -> None:
    balance = client.contract.functions.balanceOf(users[0]["address"]).call()
    print(">>> BALANCE IN WEI")
    print(balance)
    print(">>> BALANCE IN ETH")
    print(client.w3.fromWei(balance, "ether"))


# EXECUTE
test()
