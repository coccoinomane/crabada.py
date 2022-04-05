from web3 import Web3
from pprint import pprint

# VARS
currency = "ether"

# TEST FUNCTIONS
def test() -> None:
    pprint(Web3.toWei(1, currency))


# EXECUTE
test()
