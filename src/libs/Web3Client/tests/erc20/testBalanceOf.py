from typing import cast
from eth_typing import Address
from src.common.config import nodeUri, users
from src.libs.Web3Client.AvalancheCErc20Web3Client import AvalancheCErc20Web3Client
from src.helpers.general import secondOrNone
from sys import argv

# VARS
tusTokenAddress = cast(Address, "0xf693248F96Fe03422FEa95aC0aFbBBc4a8FdD172")
tokenAddress = cast(Address, secondOrNone(argv) or tusTokenAddress)

client = AvalancheCErc20Web3Client(
    nodeUri=nodeUri, privateKey=users[0]["privateKey"], contractAddress=tokenAddress
)

# TEST FUNCTIONS
def test() -> None:
    balance = client.contract.functions.balanceOf(users[0]["address"]).call()
    print(">>> BALANCE IN WEI")
    print(balance)
    print(">>> BALANCE IN ETH")
    print(client.w3.fromWei(balance, "ether"))


# EXECUTE
test()
