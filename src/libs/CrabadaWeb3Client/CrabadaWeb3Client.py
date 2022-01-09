from web3.types import TxParams, Wei
from src.libs.Web3Client.AvalancheWeb3Client import AvalancheWeb3Client
from eth_typing.encoding import HexStr

class CrabadaWeb3Client(AvalancheWeb3Client):
    """Interact with a smart contract of the game Crabada
    
    The contract resides on the Avalanche blockchain; here's the
    explorer URL:
    https://snowtrace.io/address/0x82a85407bd612f52577909f4a58bfc6873f14da8#tokentxns"""

    # TODO: We should auto-initialize contract address and ABI
    # contractAddress: str = '0x82a85407bd612f52577909f4a58bfc6873f14da8'
    # abi = json.load(abifile)
    
    def startGame(self, teamId: int) -> HexStr:
        """
        Send crabs to mine
        """
        tx: TxParams = self.buildContractTransaction(self.contract.functions.startGame(teamId))
        return self.signAndSendTransaction(tx)

    def attack(self, gameId: int, teamId: int) -> HexStr:
        """
        Attack an open mine
        """
        tx: TxParams = self.buildContractTransaction(self.contract.functions.attack(gameId, teamId))
        return self.signAndSendTransaction(tx)

    def closeGame(self, gameId: int) -> HexStr:
        """
        Close mining game, claim reward & send crabs back home
        """
        tx: TxParams = self.buildContractTransaction(self.contract.functions.closeGame(gameId))
        return self.signAndSendTransaction(tx)

    def settleGame(self, gameId: int) -> HexStr:
        """
        Close looting game, claim reward & send crabs back home
        """
        tx: TxParams = self.buildContractTransaction(self.contract.functions.settleGame(gameId))
        return self.signAndSendTransaction(tx)

    def reinforceDefense(self, gameId: int, crabadaId: int, borrowPrice: Wei) -> HexStr:
        """
        Hire a crab from the tavern to reinforce the mining team; the
        price must be expressed in Wei (1 TUS = 10^18 Wei)
        """
        tx: TxParams = self.buildContractTransaction(self.contract.functions.reinforceDefense(gameId, crabadaId, borrowPrice))
        return self.signAndSendTransaction(tx)

    def reinforceAttack(self, gameId: int, crabadaId: int, borrowPrice: Wei) -> HexStr:
        """
        Hire a crab from the tavern to reinforce the looting team;
        the price must be expressed in Wei (1 TUS = 10^18 Wei)
        """
        tx: TxParams = self.buildContractTransaction(self.contract.functions.reinforceAttack(gameId, crabadaId, borrowPrice))
        return self.signAndSendTransaction(tx)