from typing import Any, Union
from eth_typing import Address, HexStr
from web3 import Web3
from web3.types import Wei
from src.libs.Web3Client.Web3Client import Web3Client
from web3.types import TxParams, Nonce
import os


class Erc20Web3Client(Web3Client):
    """
    Client that comes with the ERC20 ABI preloaded.

    AMOUNTS
    =======

    Whenever we will refer to an "amount" of the token, we really mean an
    "amount in token units". A token unit is the smallest subdivision of
    the token. For example:
    - If the token has 6 digits (like most stablecoins) an amount of 1
      corresponds to one millionth of the token.
    - For tokens with 18 digits (like most non-stablecoins) an amount
      of 1 is equal to 1/10^18 of the token (a single wei).
    """

    abiDir = os.path.dirname(os.path.realpath(__file__)) + "/contracts"
    abi = Web3Client.getContractAbiFromFile(abiDir + "/erc20Abi.json")

    def __init__(
        self,
        nodeUri: str,
        chainId: int = None,
        txType: int = 2,
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

    ####################
    # Read
    ####################

    def balanceOf(self, address: Address) -> int:
        """
        Return the amount held by the given address
        """
        return self.contract.functions.balanceOf(address).call()

    def name(self) -> str:
        """
        Return the name/label of the token
        """
        return self.contract.functions.name().call()

    def symbol(self) -> str:
        """
        Return the symbol/ticker of the token
        """
        return self.contract.functions.symbol().call()

    def totalSupply(self) -> int:
        """
        Return the total supply of the token
        """
        return self.contract.functions.totalSupply().call()

    def decimals(self) -> int:
        """
        Return the number of digits of the token
        """
        return self.contract.functions.decimals().call()

    ####################
    # Write
    ####################

    def transfer(
        self, to: Address, amount: int, nonce: Nonce = None, valueInWei: Wei = Wei(0)
    ) -> HexStr:
        """
        Transfer some amount of the token to an address; does not
        require approval.
        """

        tx: TxParams = self.buildContractTransaction(
            self.contract.functions.transfer(Web3.toChecksumAddress(to), amount)
        )

        if nonce:
            tx["nonce"] = nonce

        if valueInWei:
            tx["value"] = valueInWei

        return self.signAndSendTransaction(tx)
