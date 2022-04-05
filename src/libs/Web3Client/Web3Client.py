from __future__ import annotations
import json
from typing import Any, Tuple, Union
from eth_account import Account
from eth_account.signers.local import LocalAccount
from eth_typing import Address
from web3 import Web3
from eth_account.datastructures import SignedTransaction
from web3.contract import ContractFunction
from web3.types import BlockData, Nonce, TxParams, TxReceipt, TxData
from eth_typing.encoding import HexStr
from src.libs.Web3Client.exceptions import MissingParameter, TransactionTooExpensive
from web3.contract import Contract


class Web3Client:
    """
    Client to interact with a blockchain, with smart contract
    support.

    The client is a wrapper the Web3 library intended to make it
    easier to use.

    Attributes
    ----------------------
    nodeUri: str = None | RPC node to use, set via
    chainId: int = None | ID of the chain
    txType: int = None | Type of transaction
    privateKey: str = None | Private key to use (optional)
    maxPriorityFeePerGasInGwei: float | Miner's tip (optional, default is 1)
    upperLimitForBaseFeeInGwei: float | Raise an exception if baseFee is larger than this (optional, default is no limit)
    contractAddress: Address | Address of smart contract (optional)
    abi: dict[str, Any] = None | ABI of smart contract; to generate from a JSON file, use static method getContractAbiFromFile() (optional)


    Derived attributes
    ------------------
    w3: Web3 = None | Web3.py client
    account: LocalAccount = None | Account object for the user
    userAddress: Address = None | Address of the user
    contract: Contract = None | Web3.py contract
    contractChecksumAddress: str = None | Check-summmed contract address

    TODO: Add support for pre-EIP-1559 transactions
    """

    def __init__(
        self,
        nodeUri: str,
        chainId: int = None,
        txType: Union[int, HexStr] = 2,
        privateKey: str = None,
        maxPriorityFeePerGasInGwei: float = 1,
        upperLimitForBaseFeeInGwei: float = float("inf"),
        contractAddress: Address = None,
        abi: dict[str, Any] = None,
    ) -> None:
        # Set attributes
        self.nodeUri: str = nodeUri
        self.chainId: int = chainId
        self.txType: Union[int, HexStr] = txType
        self.privateKey: str = privateKey
        self.maxPriorityFeePerGasInGwei: float = maxPriorityFeePerGasInGwei
        self.upperLimitForBaseFeeInGwei: float = upperLimitForBaseFeeInGwei
        self.contractAddress: Address = contractAddress
        self.abi: dict[str, Any] = abi
        # Initialize web3.py provider
        self.w3 = self.getProvider(nodeUri)
        # Initialize the contract
        if self.contractAddress and self.abi:
            self.contract = self.getContract(contractAddress, self.w3, abi=self.abi)
            self.contractChecksumAddress = Web3.toChecksumAddress(self.contractAddress)
        # Derived values
        if self.privateKey:
            self.account: LocalAccount = Account.from_key(self.privateKey)
            self.userAddress: Address = self.account.address

    ####################
    # Build Tx
    ####################

    def buildBaseTransaction(
        self,
        nonce: Nonce = None,
        gasLimit: int = None,
        maxPriorityFeePerGasInGwei: float = None,
    ) -> TxParams:
        """
        Build a basic transaction with type, nonce, chain ID and gas;
        before invoking this method you need to have specified a chainId and
        called setNodeUri().

        - If not given, the nonce will be computed on chain
        - If not given, the gas limit will be estimated on chain using gas_estimate()
        - If not given, the miner's tip (maxPriorityFeePerGas) will be set to
          self.maxPriorityFeePerGasInGwei
        - The gas price is estimated according to the usual formula
          maxMaxFeePerGas = 2 * baseFee + maxPriorityFeePerGas.
        """

        # Properties that you are not likely to change
        tx: TxParams = {
            "type": self.txType,
            "chainId": self.chainId,
            "from": self.userAddress,
        }

        # Miner's tip
        maxPriorityFeePerGasInGwei = (
            maxPriorityFeePerGasInGwei or self.maxPriorityFeePerGasInGwei
        )
        tx["maxPriorityFeePerGas"] = Web3.toWei(maxPriorityFeePerGasInGwei, "gwei")

        # Estimate the maximum price per unit of gas
        (maxFeePerGasInGwei, baseFeeInGwei) = self.estimateMaxFeePerGasInGwei(
            maxPriorityFeePerGasInGwei
        )
        tx["maxFeePerGas"] = Web3.toWei(maxFeePerGasInGwei, "gwei")

        # Raise an exception if the fee is too high
        if (
            self.upperLimitForBaseFeeInGwei is not None
            and baseFeeInGwei > self.upperLimitForBaseFeeInGwei
        ):
            raise TransactionTooExpensive(
                f"Transaction would be too expensive [baseFee={baseFeeInGwei}, max={self.upperLimitForBaseFeeInGwei}"
            )

        # If not explicitly given, fetch the nonce on chain
        tx["nonce"] = self.getNonce() if nonce is None else nonce

        # If needed, let web3 compute the gas-limit on chain.
        # For more details, see docs of ContractFunction.transact in
        # https://web3py.readthedocs.io/en/stable/contracts.html
        if gasLimit is not None:
            tx["gas"] = gasLimit  # type: ignore

        return tx

    def buildTransactionWithValue(
        self,
        to: Address,
        valueInEth: float,
        nonce: Nonce = None,
        gasLimit: int = None,
        maxPriorityFeePerGasInGwei: int = None,
    ) -> TxParams:
        """
        Build a transaction involving a transfer of value to an address,
        where the value is expressed in the blockchain token (e.g. ETH or AVAX).
        """
        tx = self.buildBaseTransaction(
            nonce,
            gasLimit,
            maxPriorityFeePerGasInGwei,
        )
        extraParams: TxParams = {
            "to": to,
            "value": self.w3.toWei(valueInEth, "ether"),
            "gas": self.estimateGasForTransfer(to, valueInEth),  # type: ignore
        }
        return tx | extraParams

    def buildContractTransaction(
        self,
        contractFunction: ContractFunction,
        nonce: Nonce = None,
        gasLimit: int = None,
        maxPriorityFeePerGasInGwei: int = None,
    ) -> TxParams:
        """
        Build a transaction that involves a contract interation.

        Requires passing the contract function as detailed in the docs:
        https://web3py.readthedocs.io/en/stable/web3.eth.account.html#sign-a-contract-transaction
        """
        baseTx = self.buildBaseTransaction(
            nonce,
            gasLimit,
            maxPriorityFeePerGasInGwei,
        )
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

    def getNonce(self, address: Address = None) -> Nonce:
        if not address:
            address = self.userAddress
        return self.w3.eth.get_transaction_count(address)

    def estimateMaxFeePerGasInGwei(
        self, maxPriorityFeePerGasInGwei: float
    ) -> Tuple[float, float]:
        """
        Estimate the maxFeePerGas parameter using the formula
        2 * baseFee + maxPriorityFeePerGas.

        This is the same formula used by web3 and here
        https://ethereum.stackexchange.com/a/113373/89782

        The baseFee is fetched on chain from the latest block.

        Returns both the estimate (in gwei) and the baseFee
        (also in gwei).
        """
        latest_block = self.w3.eth.get_block("latest")
        baseFeeInWei = latest_block["baseFeePerGas"]
        baseFeeInGwei = float(Web3.fromWei(baseFeeInWei, "gwei"))
        return (2 * baseFeeInGwei + maxPriorityFeePerGasInGwei, baseFeeInGwei)

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

    def estimateGasForTransfer(self, to: Address, valueInEth: float) -> int:
        """
        Return the gas that would be required to send some ETH
        to an address
        """
        return self.w3.eth.estimate_gas(
            {
                "from": self.userAddress,
                "to": to,
                "value": self.w3.toWei(valueInEth, "ether"),
            }
        )

    ####################
    # Static
    ####################

    @staticmethod
    def getContract(
        address: Address,
        provider: Web3,
        abiFile: str = None,
        abi: dict[str, Any] = None,
    ) -> Contract:
        """
        Load the smart contract, required before running
        buildContractTransaction().
        """
        checksum = Web3.toChecksumAddress(address)
        if abiFile:
            abi = Web3Client.getContractAbiFromFile(abiFile)
        return provider.eth.contract(address=checksum, abi=abi)

    @staticmethod
    def getContractAbiFromFile(fileName: str) -> Any:
        with open(fileName) as file:
            return json.load(file)

    @staticmethod
    def getProvider(nodeUri: str) -> Web3:
        """
        Initialize provider (HTTPS & WS supported).

        TODO: Support autodetection with empty nodeUri
        docs here https://web3py.readthedocs.io/en/stable/providers.html#how-automated-detection-works
        """
        if nodeUri[0:4] == "http":
            return Web3(Web3.HTTPProvider(nodeUri))
        elif nodeUri[0:2] == "ws":
            return Web3(Web3.WebsocketProvider(nodeUri))
        else:
            return Web3()
