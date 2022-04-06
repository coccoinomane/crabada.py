from typing import Any, Union
from eth_typing import Address, HexStr
from src.libs.Web3Client.Web3Client import Web3Client
import os


class Erc20Web3Client(Web3Client):
    """
    Client that comes with the ERC20 ABI preloaded
    """

    abiDir = os.path.dirname(os.path.realpath(__file__)) + "/contracts"
    abi = Web3Client.getContractAbiFromFile(abiDir + "/erc20Abi.json")

    def __init__(
        self,
        nodeUri: str,
        chainId: int = None,
        txType: Union[int, HexStr] = 2,
        privateKey: str = None,
        maxPriorityFeePerGasInGwei: float = 1,
        upperLimitForBaseFeeInGwei: float = float("inf"),
        contractAddress: Address = None,
    ) -> None:
        super().__init__(
            nodeUri,
            chainId,
            txType,
            privateKey,
            maxPriorityFeePerGasInGwei,
            upperLimitForBaseFeeInGwei,
            contractAddress,
            self.abi,
        )
