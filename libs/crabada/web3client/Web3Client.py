import json, os
from pprint import pprint
from web3 import Web3

class Web3Client:
    """Interact with the contract of the game Crabada
    
    The contract resides on the Avalanche blockchain; here's the
    explorer URL:
    https://snowtrace.io/address/0x82a85407bd612f52577909f4a58bfc6873f14da8#tokentxns"""

    contractAddress = '0x82a85407bd612f52577909f4a58bfc6873f14da8'
    contractChecksumAddress = None
    abi = None # contract's ABI, loaded from abi.json
    nodeUri = None # your node's URI
    w3 = None # provider Web3, vedi https://web3py.readthedocs.io/en/stable/providers.html

    def __init__(self, nodeUri: str, abiFile: str = os.path.dirname(os.path.realpath(__file__)) + '/abi.json'):
        self.contractChecksumAddress = Web3.toChecksumAddress(self.contractAddress)
        self.nodeUri = nodeUri
        self.w3 = Web3(Web3.HTTPProvider(self.nodeUri))
        self.abi = self.__loadAbi(abiFile)

    def __loadAbi(self, fileName: str):
        with open(fileName) as file:
            return json.load(file)

    def getAbi(self):
        return self.abi

    def getContract(self):
        return self.w3.eth.contract(address=self.contractChecksumAddress, abi=self.abi)

    # def startGame(self, teamId: int):
    #     """Get information from the given mine"""
    #     url = self.baseUri + '/mine/' + str(mineId)
    #     return requests.request("GET", url, params=params)

    