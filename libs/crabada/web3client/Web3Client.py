import json
from web3 import Web3
from web3.middleware import geth_poa_middleware
from pprint import pprint

class Web3Client:
    """Interact with a smart contract.
    
    Simple wrapper of the Web3 library."""

    ###################
    # TO DO: Risky
    maxPriorityFeePerGasInGwei: int = 2 # in Gwei
    gasLimit: int = 500000
    ###################
    
    contractAddress: str = None
    contractChecksumAddress: str = None
    abi: dict = None # contract's ABI, loaded from abi.json
    nodeUri: str = None # your node's URI
    w3: object = None # provider Web3, see https://web3py.readthedocs.io/en/stable/providers.html
    contract: object = None # the contract instance, see https://web3py.readthedocs.io/en/stable/examples.html#interacting-with-existing-contracts
    userAddress: str = None
    privateKey: str = None
    chainId: int = None

    ####################
    # Tx
    ####################

    def signAndSendTransaction(self, tx:dict) -> str:
        signedTx = self.signTransaction(tx)
        return self.sendSignedTransaction(signedTx)

    def signTransaction(self, tx: dict):
        """Sign the give transaction; the private key must have
        been set with setCredential().
        """
        return self.w3.eth.account.sign_transaction(tx, self.privateKey)

    def buildBaseTransaction(self) -> dict:
        """Build a basic EIP-1559 transaction with just nonce, chain ID and gas;
        you should already have called setChainId() and setNodeUri.
        
        Gas is estimated according to the formula
        maxMaxFeePerGas = 2 * baseFee + maxPriorityFeePerGas."""
        tx = {
            'type': '0x2',
            'chainId': self.chainId,
            'gas': self.gasLimit,
            'maxFeePerGas': Web3.toWei(self.estimateMaxFeePerGasInGwei(), 'gwei'),
            'maxPriorityFeePerGas': Web3.toWei(self.maxPriorityFeePerGasInGwei, 'gwei'),
            'nonce': self.getTransactionCount(),
        }
        return tx
    
    def buildTransactionWithValue(self, to: str, valueInEth: int) -> dict:
        """Build a transaction involving a transfer of value to an address,
        where the value is expressed in the blockchain token (e.g. ETH or AVAX)."""
        tx = self.buildBaseTransaction()
        return tx | { 'to': to, 'value': self.w3.toWei(valueInEth, 'ether') }

    def buildContractTransaction(self, contractFunction):
        """Build a transaction that involves a contract interation.
        
        Requires passing the contract function as detailed in the docs:
        https://web3py.readthedocs.io/en/stable/web3.eth.account.html#sign-a-contract-transaction"""
        baseTx = self.buildBaseTransaction()
        return contractFunction.buildTransaction(baseTx)

    def sendSignedTransaction(self, signedTx: object) -> str:
        """Send a signed transaction and return the tx hash"""
        tx_hash = self.w3.eth.sendRawTransaction(signedTx.rawTransaction)
        return self.w3.toHex(tx_hash)

    def getTransactionCount(self) -> int:
        return self.w3.eth.get_transaction_count(self.userAddress)

    def getNonce(self) -> int:
        return self.getTransactionCount()

    def estimateMaxFeePerGasInGwei(self) -> int:
        """Gets the base fee from the latest block and returns a maxFeePerGas
        estimate as 2 * baseFee + maxPriorityFeePerGas, as done in the
        web3 gas_price_strategy middleware (and also here >
        https://ethereum.stackexchange.com/a/113373/89782)"""
        latest_block = self.w3.eth.get_block('latest')
        baseFeeInWei = latest_block['baseFeePerGas'] # in wei
        baseFeeInGwei = Web3.fromWei(baseFeeInWei, 'gwei')
        return 2 * baseFeeInGwei + self.maxPriorityFeePerGasInGwei

    ####################
    # Setters
    ####################

    def setContract(self, contractAddress: str, abiFile: str):
        """Load the smart contract, required before running
        buildContractTransaction().

        Run only after setting the node URI (setNodeUri)"""
        self.contractAddress = contractAddress
        self.contractChecksumAddress = Web3.toChecksumAddress(contractAddress)
        self.abi = self.__getContractAbi(abiFile) # Read the contract's ABI from a JSON file
        self.contract = self.w3.eth.contract(address=self.contractChecksumAddress, abi=self.abi)
        return self

    def setNodeUri(self, nodeUri: str):
        self.nodeUri = nodeUri
        self.w3 = self.__getHttpProvider()
        ###################
        # TO DO: We should have an (IF AVAX) or (IF POA) here...
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        ###################
        return self

    def setCredentials(self, userAddress: str, privateKey: str):
        self.userAddress = userAddress
        self.privateKey = privateKey
        return self

    def setChainId(self, chainId: int):
        self.chainId = int(chainId)
        return self

    def setMaxPriorityFeePerGasInGwei(self, maxPriorityFeePerGasInGwei: int):
        self.maxPriorityFeePerGasInGwei = maxPriorityFeePerGasInGwei
        return self

    def setGasLimit(self, gasLimit: int):
        self.gasLimit = gasLimit
        return self

    ####################
    # Private
    ####################

    def __getContractAbi(self, fileName: str) -> json:
        with open(fileName) as file:
            return json.load(file)
    
    def __getHttpProvider(self) -> Web3.HTTPProvider:
        return Web3(Web3.HTTPProvider(self.nodeUri))