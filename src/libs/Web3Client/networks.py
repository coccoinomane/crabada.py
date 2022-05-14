from typing import Any, List, cast
from src.helpers.general import findInListOfDicts
from src.libs.Web3Client.exceptions import NetworkNotFound
from src.libs.Web3Client.types import NetworkConfig
from web3.middleware import geth_poa_middleware

supportedNetworks: List[NetworkConfig] = [
    # Ethereum
    {
        "name": "Ethereum",
        "txType": 1,
        "chainId": 1,
        "middlewares": [],
    },
    # Avalanche C Chain
    {
        "name": "Avalanche",
        "txType": 2,
        "chainId": 43114,
        "middlewares": [geth_poa_middleware],
    },
    # Swimmer Network Avalanche subnet
    {
        "name": "SwimmerNetwork",
        "txType": 1,
        "chainId": 73772,
        "middlewares": [geth_poa_middleware],
    },
]


def getNetworkConfig(networkName: str) -> NetworkConfig:
    """
    Return the configuration for the network with the given
    name; raises an exception if not found
    """
    network: NetworkConfig = findInListOfDicts(
        cast(Any, supportedNetworks), "name", networkName
    )
    if network is None:
        raise NetworkNotFound(f"Network '{networkName}' not supported")
    return network


def isNetworkSupported(networkName: str) -> bool:
    """
    Return true if the given network is supported by the client
    """
    try:
        getNetworkConfig(networkName)
        return True
    except NetworkNotFound:
        return False
