from typing import List, cast
from eth_account import Account
from eth_typing import Address
from hexbytes import HexBytes
from web3 import Web3
from web3.types import TxParams, Wei
from web3.exceptions import ContractLogicError
from src.libs.Web3Client.Web3Client import Web3Client
from src.libs.Web3Client.AvalancheCWeb3Client import AvalancheCWeb3Client
from eth_typing.encoding import HexStr
from src.common.logger import logger
import os
import time


class PangolinRouterWeb3Client(AvalancheCWeb3Client):
    """
     Interact with a pangolin router

     The contract resides on the Avalanche blockchain; here's
     the URL on Snowtrace:
    https://snowtrace.io/address/0xe54ca86531e17ef3616d22ca28b0d458b6c89106#code
    """

    contractAddress = cast(Address, "0xE54Ca86531e17Ef3616d22Ca28b0D458b6C89106")
    abiDir = os.path.dirname(os.path.realpath(__file__)) + "/contracts"
    abi = Web3Client.getContractAbiFromFile(abiDir + "/pangolinRouterAbi.json")

    def __init__(
        self,
        nodeUri: str,
        privateKey: str = None,
        maxPriorityFeePerGasInGwei: float = 1,
        upperLimitForBaseFeeInGwei: float = float("inf"),
    ) -> None:
        super().__init__(
            nodeUri=nodeUri,
            privateKey=privateKey,
            maxPriorityFeePerGasInGwei=maxPriorityFeePerGasInGwei,
            upperLimitForBaseFeeInGwei=upperLimitForBaseFeeInGwei,
            contractAddress=self.contractAddress,
            abi=self.abi,
        )

    def getAmountsOut(self, amtIn: int, path: list[str]) -> list[int]:
        return self.contract.functions.getAmountsOut(amtIn, path).call()

    def swapExactTokensForAvax(
        self, amtIn: int, amtOutMin: int, path: list[str]
    ) -> HexStr:
        # ensure outgoing address matches current private key
        assert self.userAddress == Account.from_key(self.privateKey).address
        assert len(path) >= 2
        # deadline is 1  min
        deadline = int(time.time() + (2 * 60))
        try:
            tx = self.buildContractTransaction(
                self.contract.functions.swapExactTokensForAVAX(
                    amtIn, amtOutMin, path, self.userAddress, deadline
                )
            )
            return self.signAndSendTransaction(tx)
        except ContractLogicError as e:
            logger.error(e)
            exit(1)
