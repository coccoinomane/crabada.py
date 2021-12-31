from .Web3Client import Web3Client

class CrabadaWeb3Client(Web3Client):
    """Interact with a smart contract of the game Crabada
    
    The contract resides on the Avalanche blockchain; here's the
    explorer URL:
    https://snowtrace.io/address/0x82a85407bd612f52577909f4a58bfc6873f14da8#tokentxns"""

    contractAddress: str = '0x82a85407bd612f52577909f4a58bfc6873f14da8'
    
    def __init__(self):
        self.setContractAddress(self.contractAddress)

    def startGame(self, teamId: int, gas: int, gasPriceInGwei: int):
        """Send crabs to mine"""
        tx = self.buildContractTransaction(
            self.contract.functions.startGame(teamId),
            gas,
            gasPriceInGwei,
        )
        signedTx = self.signTransaction(tx)
        return self.sendSignedTransaction(signedTx)
