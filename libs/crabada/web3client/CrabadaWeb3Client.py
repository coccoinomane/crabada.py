from .Web3Client import Web3Client

class CrabadaWeb3Client(Web3Client):
    """Interact with a smart contract of the game Crabada
    
    The contract resides on the Avalanche blockchain; here's the
    explorer URL:
    https://snowtrace.io/address/0x82a85407bd612f52577909f4a58bfc6873f14da8#tokentxns"""

    # TODO: We should auto-initialize contract address and ABI
    # contractAddress: str = '0x82a85407bd612f52577909f4a58bfc6873f14da8'
    # abi = json.load(abifile)
    
    def startGame(self, teamId: int):
        """Send crabs to mine"""
        tx = self.buildContractTransaction(self.contract.functions.startGame(teamId))
        return self.signAndSendTransaction(tx)

    def closeGame(self, gameId: int):
        """Claim reward & send crabs back home"""
        tx = self.buildContractTransaction(self.contract.functions.closeGame(gameId))
        return self.signAndSendTransaction(tx)
