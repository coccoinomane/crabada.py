from web3 import Web3
from web3.types import Wei

def tusToWei(tus: int) -> Wei:
    """
    Convert TUS to Wei; this is required before making comparisons
    because the Crabada APIs (both Web2 and Web3) always return Wei.
    
    The conversion is 1 TUS = 10^18 Wei.
    """
    return Web3.toWei(tus, 'ether')

def weiToTus(wei: Wei) -> int:
    """
    Convert Wei to TUS
    """
    return Web3.fromWei(wei, 'ether')