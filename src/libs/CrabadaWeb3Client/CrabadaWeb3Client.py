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
        """Send crabs to mine"""
        tx: TxParams = self.buildContractTransaction(self.contract.functions.startGame(teamId))
        return self.signAndSendTransaction(tx)

    def closeGame(self, gameId: int) -> HexStr:
        """Claim reward & send crabs back home"""
        tx: TxParams = self.buildContractTransaction(self.contract.functions.closeGame(gameId))
        return self.signAndSendTransaction(tx)

    def reinforceDefense(self, gameId: int, crabadaId: int, borrowPrice: Wei) -> HexStr:
        """Hire a crab from the tavern; the price must be expressed in
        units of 1e-18 TUS. This means that price=1000000000000000000
        is just 1 TUS"""
        tx: TxParams = self.buildContractTransaction(self.contract.functions.reinforceDefense(gameId, crabadaId, borrowPrice))
        return self.signAndSendTransaction(tx)