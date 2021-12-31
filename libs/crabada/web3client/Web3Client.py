import json, os
from pprint import pprint
from web3 import Web3

class Web3Client:
    """Interact with a smart contract of the game Crabada
    
    The contract resides on the Avalanche blockchain; here's the
    explorer URL:
    https://snowtrace.io/address/0x82a85407bd612f52577909f4a58bfc6873f14da8#tokentxns"""

    contractAddress: str = None
    contractChecksumAddress: str = None
    abi: dict = None # contract's ABI, loaded from abi.json
    nodeUri: str = None # your node's URI
    w3: object = None # provider Web3, see https://web3py.readthedocs.io/en/stable/providers.html
    contract: object = None # the contract interface  provider Web3, see https://web3py.readthedocs.io/en/stable/contracts.html
    userAddress: str = None
    privateKey: str = None

    ####################
    # Routes
    ####################

    # def startGame(self, teamId: int):
    #     """Get information from the given mine"""
    #     url = self.baseUri + '/mine/' + str(mineId)
    #     return requests.request("GET", url, params=params)

    ####################
    # Setters
    ####################

    def setContractAddress(self, contractAddress: str):
        self.contractAddress = contractAddress
        self.contractChecksumAddress = Web3.toChecksumAddress(contractAddress)
        return self

    def setNodeUri(self, nodeUri: str):
        self.nodeUri = nodeUri
        return self

    def setCredentials(self, userAddress: str, privateKey: str):
        self.userAddress = userAddress
        self.privateKey = privateKey
        return self

    def setAbi(self, fileName: str):
        """Read the contract's ABI from a JSON file"""
        self.abi = self.__loadAbi(fileName)
        return self

    def init(self):
        """Makes the contract ready to be used by the client.
        
        Run only after:
        - setting the node URI (setNodeUri)
        - set the contract's address (setContractAddress)
        - set the contract's ABI (setAbi)."""
        self.w3 = Web3(Web3.HTTPProvider(self.nodeUri))
        self.contract = self.w3.eth.contract(address=self.contractChecksumAddress, abi=self.abi)
        return self

    ####################
    # Private
    ####################

    def __loadAbi(self, fileName: str):
        with open(fileName) as file:
            return json.load(file)