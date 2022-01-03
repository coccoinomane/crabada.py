from __future__ import annotations
import json
from typing import Any
from eth_typing import Address
from web3 import Web3
from eth_account.datastructures import SignedTransaction
from web3.contract import Contract, ContractFunction
from web3.types import Nonce, TxParams, TxReceipt
from eth_typing.encoding import HexStr

class Web3Client:
    """Client to interact with a blockchain, with smart
    contract support.
    
    Wrapper of the Web3 library intended to make it easier
    to use."""

    maxPriorityFeePerGasInGwei: int = None
    gasLimit: int = None    
    contractAddress: Address = None
    contractChecksumAddress: str = None
    abi: dict[str, Any] = None # contract's ABI, loaded from abi.json
    nodeUri: str = None # your node's URI
    w3: Web3 = None # provider Web3, see https://web3py.readthedocs.io/en/stable/providers.html
    contract: Contract = None # the contract instance, see https://web3py.readthedocs.io/en/stable/examples.html#interacting-with-existing-contracts
    userAddress: Address = None
    privateKey: str = None
    chainId: int = None

    ####################
    # Build Tx
    ####################

    def buildBaseTransaction(self) -> TxParams:
        """Build a basic EIP-1559 transaction with just nonce, chain ID and gas;
        you should already have called setChainId() and setNodeUri.
        
        Gas is estimated according to the formula
        maxMaxFeePerGas = 2 * baseFee + maxPriorityFeePerGas."""
        tx: TxParams = {
            'type': 0x2,
            'chainId': self.chainId,
            'gas': self.gasLimit, # type: ignore
            'maxFeePerGas': Web3.toWei(self.estimateMaxFeePerGasInGwei(), 'gwei'),
            'maxPriorityFeePerGas': Web3.toWei(self.maxPriorityFeePerGasInGwei, 'gwei'),
            'nonce': self.getNonce(),
        }
        return tx
    
    def buildTransactionWithValue(self, to: Address, valueInEth: float) -> TxParams:
        """Build a transaction involving a transfer of value to an address,
        where the value is expressed in the blockchain token (e.g. ETH or AVAX)."""
        tx = self.buildBaseTransaction()
        txValue: TxParams = { 'to': to, 'value': self.w3.toWei(valueInEth, 'ether') }
        return tx | txValue

    def buildContractTransaction(self, contractFunction: ContractFunction) -> TxParams:
        """Build a transaction that involves a contract interation.
        
        Requires passing the contract function as detailed in the docs:
        https://web3py.readthedocs.io/en/stable/web3.eth.account.html#sign-a-contract-transaction"""
        baseTx = self.buildBaseTransaction()
        return contractFunction.buildTransaction(baseTx)

    ####################
    # Sign & send Tx
    ####################

    def signTransaction(self, tx: TxParams) -> SignedTransaction:
        """Sign the give transaction; the private key must have
        been set with setCredential().
        """
        return self.w3.eth.account.sign_transaction(tx, self.privateKey)

    def sendSignedTransaction(self, signedTx: SignedTransaction) -> HexStr:
        """Send a signed transaction and return the tx hash"""
        tx_hash = self.w3.eth.send_raw_transaction(signedTx.rawTransaction)
        return self.w3.toHex(tx_hash)

    def signAndSendTransaction(self, tx: TxParams) -> HexStr:
        """Sign a transaction and send it"""
        signedTx = self.signTransaction(tx)
        return self.sendSignedTransaction(signedTx)
    
    def getTransactionReceipt(self, txHash: HexStr) -> TxReceipt:
        """Given a transaction, wait for the blockchain to confirm
        it and return the tx receipt."""
        return self.w3.eth.wait_for_transaction_receipt(txHash)

    ####################
    # Utils
    ####################

    def getNonce(self) -> Nonce:
        return self.w3.eth.get_transaction_count(self.userAddress)

    def estimateMaxFeePerGasInGwei(self) -> int:
        """Gets the base fee from the latest block and returns a maxFeePerGas
        estimate as 2 * baseFee + maxPriorityFeePerGas, as done in the
        web3 gas_price_strategy middleware (and also here >
        https://ethereum.stackexchange.com/a/113373/89782)"""
        latest_block = self.w3.eth.get_block('latest')
        baseFeeInWei = latest_block['baseFeePerGas'] # in wei
        baseFeeInGwei = int(Web3.fromWei(baseFeeInWei, 'gwei'))
        return 2 * baseFeeInGwei + self.maxPriorityFeePerGasInGwei

    ####################
    # Setters
    ####################

    def setContract(self, contractAddress: Address, abiFile: str) -> Web3Client:
        """Load the smart contract, required before running
        buildContractTransaction().

        Run only after setting the node URI (setNodeUri)"""
        self.contractAddress = contractAddress
        self.contractChecksumAddress = Web3.toChecksumAddress(contractAddress)
        self.abi = self.__getContractAbi(abiFile) # Read the contract's ABI from a JSON file
        self.contract = self.w3.eth.contract(address=self.contractChecksumAddress, abi=self.abi)
        return self

    def setNodeUri(self, nodeUri: str) -> Web3Client:
        self.nodeUri = nodeUri
        self.w3 = self.__getHttpProvider()
        return self

    def setCredentials(self, userAddress: Address, privateKey: str) -> Web3Client:
        self.userAddress = userAddress
        self.privateKey = privateKey
        return self

    def setChainId(self, chainId: int) -> Web3Client:
        self.chainId = int(chainId)
        return self

    def setMaxPriorityFeePerGasInGwei(self, maxPriorityFeePerGasInGwei: int) -> Web3Client:
        self.maxPriorityFeePerGasInGwei = maxPriorityFeePerGasInGwei
        return self

    def setGasLimit(self, gasLimit: int) -> Web3Client:
        self.gasLimit = gasLimit
        return self

    ####################
    # Private
    ####################

    def __getContractAbi(self, fileName: str) -> Any:
        with open(fileName) as file:
            return json.load(file)
    
    def __getHttpProvider(self) -> Web3:
        return Web3(Web3.HTTPProvider(self.nodeUri))
