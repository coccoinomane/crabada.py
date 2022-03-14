from __future__ import annotations
import json
from typing import Any, Dict, Optional, Sequence
from eth_account import Account
from eth_typing import Address, BlockIdentifier, ChecksumAddress
from web3 import Web3
from eth_account.datastructures import SignedTransaction
from web3.contract import Contract, ContractFunction
from web3.types import BlockData, Nonce, TxParams, TxReceipt, TxData
from eth_typing.encoding import HexStr
from src.libs.Web3Client.exceptions import MissingParameter


class Web3Client:
    """
    Client to interact with a blockchain, with smart
    contract support.

    Wrapper of the Web3 library intended to make it easier
    to use.

    Attributes
    ----------
    maxPriorityFeePerGasInGwei : int
    gasLimit : int
    contractAddress : Address
    abi: dict[str, Any] = None
    chainId: int = None
    nodeUri: str = None
    userAddress: Address = None
    privateKey: str = None

    Derived attributes
    ----------
    contractChecksumAddress: str = None
    w3: Web3 = None
    contract: Contract = None
    """

    ####################
    # Build Tx
    ####################

    def buildBaseTransaction(self) -> TxParams:
        """
        Build a basic EIP-1559 transaction with just nonce, chain ID and gas;
        before invoking this method you need to have specified a chainId and
        called setNodeUri().

        Gas is estimated according to the formula
        maxMaxFeePerGas = 2 * baseFee + maxPriorityFeePerGas.
        """
        tx: TxParams = {
            "type": 0x2,
            "chainId": self.chainId,
            "gas": self.gasLimit,  # type: ignore
            "maxFeePerGas": Web3.toWei(self.estimateMaxFeePerGasInGwei(), "gwei"),
            "maxPriorityFeePerGas": Web3.toWei(self.maxPriorityFeePerGasInGwei, "gwei"),
            "nonce": self.getNonce(),
        }
        return tx

    def buildTransactionWithValue(self, to: Address, valueInEth: float) -> TxParams:
        """
        Build a transaction involving a transfer of value to an address,
        where the value is expressed in the blockchain token (e.g. ETH or AVAX).
        """
        tx = self.buildBaseTransaction()
        txValue: TxParams = {"to": to, "value": self.w3.toWei(valueInEth, "ether")}
        return tx | txValue

    def buildContractTransaction(self, contractFunction: ContractFunction) -> TxParams:
        """
        Build a transaction that involves a contract interation.

        Requires passing the contract function as detailed in the docs:
        https://web3py.readthedocs.io/en/stable/web3.eth.account.html#sign-a-contract-transaction
        """
        baseTx = self.buildBaseTransaction()
        return contractFunction.buildTransaction(baseTx)

    ####################
    # Sign & send Tx
    ####################

    def signTransaction(self, tx: TxParams) -> SignedTransaction:
        """
        Sign the give transaction; the private key must have
        been set with setCredential().
        """
        return self.w3.eth.account.sign_transaction(tx, self.privateKey)

    def sendSignedTransaction(self, signedTx: SignedTransaction) -> HexStr:
        """
        Send a signed transaction and return the tx hash
        """
        tx_hash = self.w3.eth.send_raw_transaction(signedTx.rawTransaction)
        return self.w3.toHex(tx_hash)

    def signAndSendTransaction(self, tx: TxParams) -> HexStr:
        """
        Sign a transaction and send it
        """
        signedTx = self.signTransaction(tx)
        return self.sendSignedTransaction(signedTx)

    def getTransactionReceipt(self, txHash: HexStr) -> TxReceipt:
        """
        Given a transaction hash, wait for the blockchain to confirm
        it and return the tx receipt.
        """
        return self.w3.eth.wait_for_transaction_receipt(txHash)

    def getTransaction(self, txHash: HexStr) -> TxData:
        """
        Given a transaction hash, get the transaction; will raise error
        if the transaction has not been mined yet.
        """
        return self.w3.eth.get_transaction(txHash)

    ####################
    # Watch
    ####################

    # def watch(
    #         eventName: str,
    #         argument_filters: Optional[Dict[str, Any]] = None,
    #         fromBlock: Optional[BlockIdentifier] = None,
    #         toBlock: BlockIdentifier = "latest",
    #         address: Optional[ChecksumAddress] = None,
    #         topics: Optional[Sequence[Any]] = None) -> None:
    #     """
    #     Watch for a certain event
    #     """
    #     method_to_call = getattr(foo, 'bar')
    #     result = method_to_call()
    #     event = client.contract.events.StartGame()
    #     filter = event.createFilter(fromBlock='latest' ...)

    ####################
    # Utils
    ####################

    def getNonce(self, address: str = None) -> Nonce:
        if not address:
            address = self.userAddress
        return self.w3.eth.get_transaction_count(address)

    def estimateMaxFeePerGasInGwei(self) -> int:
        """
        Gets the base fee from the latest block and returns a maxFeePerGas
        estimate as 2 * baseFee + maxPriorityFeePerGas, as done in the
        web3 gas_price_strategy middleware (and also here >
        https://ethereum.stackexchange.com/a/113373/89782)
        """
        latest_block = self.w3.eth.get_block("latest")
        baseFeeInWei = latest_block["baseFeePerGas"]  # in wei
        baseFeeInGwei = int(Web3.fromWei(baseFeeInWei, "gwei"))
        return 2 * baseFeeInGwei + self.maxPriorityFeePerGasInGwei

    def getLatestBlock(self) -> BlockData:
        """
        Return the latest block
        """
        return self.w3.eth.get_block("latest")

    def getPendingBlock(self) -> BlockData:
        """
        Return the pending block
        """
        return self.w3.eth.get_block("pending")

    ####################
    # Setters
    ####################

    def setContract(
        self, address: Address, abiFile: str = None, abi: dict[str, Any] = None
    ) -> Web3Client:
        """
        Load the smart contract, required before running
        buildContractTransaction().

        Run only after setting the node URI (setNodeUri)
        """
        self.contractAddress = address
        self.contractChecksumAddress = Web3.toChecksumAddress(address)
        if abiFile:  # Read the contract's ABI from a JSON file
            self.abi = self.getContractAbiFromFile(abiFile)
        elif abi:  # read the contract's ABI from a string
            self.abi = abi
        if not self.abi:
            raise MissingParameter("Missing ABI")
        self.contract = self.w3.eth.contract(
            address=self.contractChecksumAddress, abi=self.abi
        )
        return self

    def setNodeUri(self, nodeUri: str = None) -> Web3Client:
        """
        Set node URI and initalize provider (HTTPS & WS supported).

        Provide an empty nodeUri to use autodetection,
        docs here https://web3py.readthedocs.io/en/stable/providers.html#how-automated-detection-works
        """
        self.nodeUri = nodeUri
        self.w3 = self.getProvider()
        # Set the contract if possible, e.g. if the subclass defines address & ABI.
        try:
            self.setContract(address=self.contractAddress, abi=self.abi)
        except:
            pass
        return self

    def setCredentials(self, privateKey: str) -> Web3Client:
        self.privateKey = privateKey
        account = Account.from_key(self.privateKey)
        self.userAddress = account.address
        return self

    def setChainId(self, chainId: int) -> Web3Client:
        self.chainId = int(chainId)
        return self

    def setMaxPriorityFeePerGasInGwei(
        self, maxPriorityFeePerGasInGwei: int
    ) -> Web3Client:
        self.maxPriorityFeePerGasInGwei = maxPriorityFeePerGasInGwei
        return self

    def setGasLimit(self, gasLimit: int) -> Web3Client:
        self.gasLimit = gasLimit
        return self

    ####################
    # Protected
    ####################

    @staticmethod
    def getContractAbiFromFile(fileName: str) -> Any:
        with open(fileName) as file:
            return json.load(file)

    def getProvider(self) -> Web3:
        if self.nodeUri[0:4] == "http":
            return Web3(Web3.HTTPProvider(self.nodeUri))
        elif self.nodeUri[0:2] == "ws":
            return Web3(Web3.WebsocketProvider(self.nodeUri))
        else:
            return Web3()
