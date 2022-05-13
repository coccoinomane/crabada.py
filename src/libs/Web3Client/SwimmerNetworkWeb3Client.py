from typing import Any
from eth_typing import Address, HexStr
from src.libs.Web3Client.Web3Client import Web3Client
from web3.middleware import geth_poa_middleware


class SwimmerNetworkWeb3Client(Web3Client):
    """
    Client to interact with the Swimmer Network (subnet of Avalanche)
    and its smart contracts.
    """

    chainId = 73772
    txType = 1

    def __init__(
        self,
        nodeUri: str,
        privateKey: str = None,
        maxPriorityFeePerGasInGwei: float = 1,
        upperLimitForBaseFeeInGwei: float = float("inf"),
        contractAddress: Address = None,
        abi: dict[str, Any] = None,
    ) -> None:
        super().__init__(
            nodeUri=nodeUri,
            privateKey=privateKey,
            chainId=self.chainId,
            txType=self.txType,
            maxPriorityFeePerGasInGwei=maxPriorityFeePerGasInGwei,
            upperLimitForBaseFeeInGwei=upperLimitForBaseFeeInGwei,
            contractAddress=contractAddress,
            abi=abi,
        )
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
