from typing import Any, Union
from eth_typing import Address, HexStr
from src.libs.Web3Client.Web3Client import Web3Client
import os

from src.libs.Web3Client.Erc20Web3Client import Erc20Web3Client
from src.libs.Web3Client.AvalancheCWeb3Client import AvalancheCWeb3Client


class AvalancheCErc20Web3Client(AvalancheCWeb3Client):
    """
    Avalanche client that comes with the ERC20 ABI preloaded
    """

    abiDir = os.path.dirname(os.path.realpath(__file__)) + "/contracts"
    abi = Web3Client.getContractAbiFromFile(abiDir + "/erc20Abi.json")

    def __init__(
        self,
        nodeUri: str,
        privateKey: str = None,
        maxPriorityFeePerGasInGwei: float = 1,
        upperLimitForBaseFeeInGwei: float = float("inf"),
        contractAddress: Address = None,
    ) -> None:
        super().__init__(
            nodeUri=nodeUri,
            privateKey=privateKey,
            maxPriorityFeePerGasInGwei=maxPriorityFeePerGasInGwei,
            upperLimitForBaseFeeInGwei=upperLimitForBaseFeeInGwei,
            contractAddress=contractAddress,
            abi=self.abi,
        )
