from typing import cast
from eth_typing import Address
from hexbytes import HexBytes
from web3.types import TxParams, Wei
from src.libs.Web3Client.Web3Client import Web3Client
from src.libs.Web3Client.SwimmerNetworkWeb3Client import SwimmerNetworkWeb3Client
from eth_typing.encoding import HexStr
import os


class CrabadaWeb3Client(SwimmerNetworkWeb3Client):
    """
    Interact with a smart contract of the game Crabada

    The contract resides on the Swimmer Network subnet blockchain;
    here's the URL on Subnet explorer:
    https://subnets.avax.network/swimmer/mainnet/explorer/address/0x9ab9e81Be39b73de3CCd9408862b1Fc6D2144d2B
    """

    contractAddress = cast(Address, "0x9ab9e81Be39b73de3CCd9408862b1Fc6D2144d2B")
    abiDir = os.path.dirname(os.path.realpath(__file__)) + "/contracts"
    abi = Web3Client.getContractAbiFromFile(abiDir + "/IdleGameAbi.json")

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

    def startGame(self, teamId: int) -> HexStr:
        """
        Send crabs to mine
        """
        tx: TxParams = self.buildContractTransaction(
            self.contract.functions.startGame(teamId),
        )
        return self.signAndSendTransaction(tx)

    def attack(
        self, gameId: int, teamId: int, expiredTime: int, certificate: HexBytes
    ) -> HexStr:
        """
        Attack an open mine
        """
        tx: TxParams = self.buildContractTransaction(
            self.contract.functions.attack(gameId, teamId, expiredTime, certificate),
        )
        return self.signAndSendTransaction(tx)

    def closeGame(self, gameId: int) -> HexStr:
        """
        Close mining game, claim reward & send crabs back home
        """
        tx: TxParams = self.buildContractTransaction(
            self.contract.functions.closeGame(gameId),
        )
        return self.signAndSendTransaction(tx)

    def settleGame(self, gameId: int) -> HexStr:
        """
        Close looting game, claim reward & send crabs back home
        """
        tx: TxParams = self.buildContractTransaction(
            self.contract.functions.settleGame(gameId),
        )
        return self.signAndSendTransaction(tx)

    def reinforceDefense(self, gameId: int, crabadaId: int, borrowPrice: Wei) -> HexStr:
        """
        Hire a crab from the tavern to reinforce the mining team; the
        price must be expressed in Wei (1 TUS = 10^18 Wei)
        """
        tx: TxParams = self.buildContractTransaction(
            self.contract.functions.reinforceDefense(gameId, crabadaId, borrowPrice),
            valueInWei=borrowPrice,
        )
        return self.signAndSendTransaction(tx)

    def reinforceAttack(self, gameId: int, crabadaId: int, borrowPrice: Wei) -> HexStr:
        """
        Hire a crab from the tavern to reinforce the looting team;
        the price must be expressed in Wei (1 TUS = 10^18 Wei)
        """
        tx: TxParams = self.buildContractTransaction(
            self.contract.functions.reinforceAttack(gameId, crabadaId, borrowPrice),
            valueInWei=borrowPrice,
        )
        return self.signAndSendTransaction(tx)
