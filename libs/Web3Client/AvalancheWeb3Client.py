from libs.Web3Client.Web3Client import Web3Client
from web3.middleware import geth_poa_middleware

class AvalancheWeb3Client(Web3Client):
    """Client to interact with the Avalanche blockchain and
    its smart contracts."""

    def setNodeUri(self, nodeUri: str):
        """Inject the POA middleware"""
        super().setNodeUri(nodeUri)
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        return self
