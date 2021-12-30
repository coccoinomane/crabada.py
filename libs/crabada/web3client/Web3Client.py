import requests

class Web2Client:
    """Interact with the contract of the game Crabada
    
    The contract resides on the Avalanche blockchain; here's the
    explorer URL:
    https://snowtrace.io/address/0x82a85407bd612f52577909f4a58bfc6873f14da8#tokentxns"""

    contract = '0x82a85407bd612f52577909f4a58bfc6873f14da8'
    w3 = Web3(Web3.HTTPProvider('https://avalanche--mainnet--rpc.datahub.figment.io/apikey/YOUR_KEY/ext/bc/C/rpc'))

    def startGame(self, teamId: int):
        """Get information from the given mine"""
        url = self.baseUri + '/mine/' + str(mineId)
        return requests.request("GET", url, params=params)