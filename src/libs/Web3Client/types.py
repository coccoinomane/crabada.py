from typing import List, TypedDict
from web3.types import Middleware


class NetworkConfig(TypedDict):
    """
    Dictionary representing the configuration of a network, e.g. Ethereum,
    Avalanche, etc.
    """

    name: str
    txType: int
    chainId: int
    middlewares: List[Middleware]
