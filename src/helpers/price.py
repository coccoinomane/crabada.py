from typing import cast
from web3 import Web3
from web3.types import Wei

from src.common.types import Tus, Cra


def tusToWei(tus: float) -> Wei:
    """
    Convert TUS to Wei; this is required before making comparisons
    because the Crabada APIs (both Web2 and Web3) always return Wei.

    The conversion is 1 TUS = 10^18 Wei.
    """
    return Web3.toWei(tus, "ether")


def weiToTus(wei: Wei) -> Tus:
    """
    Convert Wei to TUS
    """
    return cast(Tus, Web3.fromWei(wei, "ether"))


def craToWei(cra: float) -> Wei:
    """
    Convert CRA to Wei
    """
    return Web3.toWei(cra, "ether")


def weiToCra(wei: Wei) -> Cra:
    """
    Convert Wei to CRA
    """
    return cast(Cra, Web3.fromWei(wei, "ether"))
