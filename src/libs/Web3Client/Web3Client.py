import json
from typing import Any, List, Tuple, cast, Union
from eth_account import Account
from eth_account.signers.local import LocalAccount
from eth_typing import Address
from hexbytes import HexBytes
from web3 import Web3
from eth_account.datastructures import SignedTransaction
from web3.contract import ContractFunction
from web3.types import BlockData, Nonce, TxParams, TxReceipt, TxData
from eth_typing.encoding import HexStr
from src.libs.Web3Client.exceptions import TransactionTooExpensive
from web3.contract import Contract
from web3.types import Middleware, Wei
from web3.gas_strategies import rpc


class Web3Client:
    """
    Client to interact with a blockchain, with smart contract
    support.

    The client is a wrapper intended to make the Web3 library
    easier to use.

    There are two ways to use the client:
    1. CUSTOM: Extend the Web3Client class to support different types of blockchains
       and smart contracts.
    2. AUTOMATIC: Use the 'make' methods in Web3ClientFactory.py to create
       clients pre-configured for different blockchains and different
       contracts.

    Attributes
    ----------------------
    nodeUri: str | RPC node to use
    chainId: int = None | ID of the chain
    txType: int = 2 | Type of transaction
    privateKey: str = None | Private key to use (optional)
    maxPriorityFeePerGasInGwei: float = 1 | Miner's tip, relevant only for type-2 transactions (optional, default is 1)
    upperLimitForBaseFeeInGwei: float = inf | Raise an exception if baseFee is larger than this (optional, default is no limit)
    contractAddress: Address = None | Address of smart contract (optional)
    abi: dict[str, Any] = None | ABI of smart contract; to generate from a JSON file, use static method getContractAbiFromFile() (optional)
    middlewares: List[Middleware] = [] | Ordered list of web3.py middlewares to use (optional, default is no middlewares)


    Derived attributes
    ------------------
    w3: Web3 = None | Web3.py client
    account: LocalAccount = None | Account object for the user
    userAddress: Address = None | Address of the user
    contract: Contract = None | Contract object of web3.py
    """

    def __init__(
        self,
        nodeUri: str,
        chainId: int = None,
        txType: int = 2,
        privateKey: str = None,
        maxPriorityFeePerGasInGwei: float = 1,
        upperLimitForBaseFeeInGwei: float = float("inf"),
        contractAddress: Address = None,
        abi: dict[str, Any] = None,
        middlewares: List[Middleware] = [],
    ) -> None:
        # Set attributes
        self.chainId: int = chainId
        self.txType: int = txType
        self.maxPriorityFeePerGasInGwei: float = maxPriorityFeePerGasInGwei
        self.upperLimitForBaseFeeInGwei: float = upperLimitForBaseFeeInGwei
        # Initialize web3.py provider
        if nodeUri:
            self.setProvider(nodeUri)
        # User account
        if privateKey:
            self.setAccount(privateKey)
        # Initialize the contract
        # TODO: we should be able to load an ABI without a specific address.
        # This might be useful to access the ABI decoding functions of web3.
        # For example, to read events from a tx only the ABI is needed, you
        # do not need the token address.
        if contractAddress and abi:
            self.setContract(contractAddress, abi)
        # Add web3.py middlewares
        if middlewares:
            self.setMiddlewares(middlewares)

    ####################
    # Setters
    ####################

    def setProvider(self, nodeUri: str) -> None:
        self.nodeUri: str = nodeUri
        self.w3 = self.getProvider(nodeUri)

    def setAccount(self, privateKey: str) -> None:
        self.privateKey: str = privateKey
        self.account: LocalAccount = Account.from_key(privateKey)
        self.userAddress: Address = self.account.address

    def setContract(self, contractAddress: Address, abi: dict[str, Any]) -> None:
        self.contractAddress: Address = cast(
            Address, Web3.toChecksumAddress(contractAddress)
        )
        self.abi: dict[str, Any] = abi
        self.contract = self.getContract(contractAddress, self.w3, abi=abi)

    def setMiddlewares(self, middlewares: List[Middleware]) -> None:
        self.middlewares: List[Middleware] = middlewares
        for (i, m) in enumerate(middlewares):
            self.w3.middleware_onion.inject(m, layer=i)

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
        Build a basic transaction with type, nonce, chain ID and gas

        - If not given, the nonce will be computed on chain
        - If not given, the gas limit will be estimated on chain using gas_estimate()
        - For type-2 transactions, if not given, the miner's tip (maxPriorityFeePerGas)
          will be set to self.maxPriorityFeePerGasInGwei
        - For type-2 transactions, the max gas fee is estimated according to the usual
          formula maxMaxFeePerGas = 2 * baseFee + maxPriorityFeePerGas.
        - For type-1 transactions, the gasPrice is estimated on-chain using eth_gasPrice.
        """

        # Properties that you are not likely to change
        tx: TxParams = {
            "type": self.txType,
            "chainId": self.chainId,
            "from": self.userAddress,
        }

        # Compute gas fee based on the transaction type
        gasFeeInGwei: float = None

        # Pre EIP-1599, we only have gasPrice
        if self.txType == 1:
            self.w3.eth.set_gas_price_strategy(rpc.rpc_gas_price_strategy)
            tx["gasPrice"] = self.w3.eth.generate_gas_price()
            gasFeeInGwei = float(Web3.fromWei(tx["gasPrice"], "gwei"))

        # Post EIP-1599, we have both the miner's tip and the max fee.
        elif self.txType == 2:

            # The miner tip is user-provided
            maxPriorityFeePerGasInGwei = (
                maxPriorityFeePerGasInGwei or self.maxPriorityFeePerGasInGwei
            )
            tx["maxPriorityFeePerGas"] = Web3.toWei(maxPriorityFeePerGasInGwei, "gwei")

            # The max fee is estimated from the miner tip & block base fee
            (maxFeePerGasInGwei, gasFeeInGwei) = self.estimateMaxFeePerGasInGwei(
                maxPriorityFeePerGasInGwei
            )
            tx["maxFeePerGas"] = Web3.toWei(maxFeePerGasInGwei, "gwei")

        # Raise an exception if the fee is too high
        self.raiseIfGasFeeTooHigh(gasFeeInGwei)

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
        Build a transaction involving a transfer of value (in ETH) to an address,
        where the value is expressed in the blockchain token (e.g. ETH or AVAX).
        """
        valueInWei = self.w3.toWei(valueInEth, "ether")
        return self.buildTransactionWithValueInWei(
            to, valueInWei, nonce, gasLimit, maxPriorityFeePerGasInGwei
        )

    def buildTransactionWithValueInWei(
        self,
        to: Address,
        valueInWei: Wei,
        nonce: Nonce = None,
        gasLimit: int = None,
        maxPriorityFeePerGasInGwei: int = None,
    ) -> TxParams:
        """
        Build a transaction involving a transfer of value (in Wei) to an address,
        where the value is expressed in the blockchain token (e.g. ETH or AVAX).
        """
        tx = self.buildBaseTransaction(
            nonce,
            gasLimit,
            maxPriorityFeePerGasInGwei,
        )
        extraParams: TxParams = {
            "to": to,
            "value": valueInWei,
            "gas": self.estimateGasForTransfer(to, valueInWei),  # type: ignore
        }
        return tx | extraParams

    def buildContractTransaction(
        self,
        contractFunction: ContractFunction,
        valueInWei: Wei = None,
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
        if valueInWei:
            baseTx["value"] = valueInWei
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

    def getTransaction(self, txHash: Union[HexStr, HexBytes]) -> TxData:
        """
        Given a transaction hash, get the transaction; will raise error
        if the transaction has not been mined yet.
        """
        return self.w3.eth.get_transaction(txHash)

    def sendEth(
        self,
        to: Address,
        valueInEth: float,
        nonce: Nonce = None,
        gasLimit: int = None,
        maxPriorityFeePerGasInGwei: int = None,
    ) -> HexStr:
        """
        Send ETH to the given address
        """
        tx = self.buildTransactionWithValue(
            to, valueInEth, nonce, gasLimit, maxPriorityFeePerGasInGwei
        )
        return self.signAndSendTransaction(tx)

    def sendEthInWei(
        self,
        to: Address,
        valueInWei: Wei,
        nonce: Nonce = None,
        gasLimit: int = None,
        maxPriorityFeePerGasInGwei: int = None,
    ) -> HexStr:
        """
        Send ETH (in Wei) to the given address
        """
        tx = self.buildTransactionWithValueInWei(
            to, valueInWei, nonce, gasLimit, maxPriorityFeePerGasInGwei
        )
        return self.signAndSendTransaction(tx)

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
    # Gas
    ####################

    def estimateMaxFeePerGasInGwei(
        self, maxPriorityFeePerGasInGwei: float
    ) -> Tuple[float, float]:
        """
        For Type-2 transactions (post EIP-1559), estimate the maxFeePerGas
        parameter using the formula 2 * baseFee + maxPriorityFeePerGas.

        This is the same formula used by web3 and here
        https://ethereum.stackexchange.com/a/113373/89782

        The baseFee is fetched on chain from the latest block.

        Returns both the estimate (in gwei) and the baseFee
        (also in gwei).
        """
        latestBlock = self.w3.eth.get_block("latest")
        baseFeeInWei = latestBlock["baseFeePerGas"]
        baseFeeInGwei = float(Web3.fromWei(baseFeeInWei, "gwei"))
        return (2 * baseFeeInGwei + maxPriorityFeePerGasInGwei, baseFeeInGwei)

    def estimateGasPriceInGwei(self) -> float:
        """
        For Type-1 transactions (pre EIP-1559), estimate the gasPrice
        parameter by asking it directly to the node.

        Docs: https://web3py.readthedocs.io/en/stable/gas_price.html
        """
        self.w3.eth.set_gas_price_strategy(rpc.rpc_gas_price_strategy)
        return float(Web3.fromWei(self.w3.eth.generate_gas_price(), "gwei"))

    def raiseIfGasFeeTooHigh(self, gasFeeInGwei: float) -> None:
        """
        Raise an exception if the given gas fee in Gwei is too high.

        For Type-1 transactions, pass the gasPrice; for Type-2,
        pass the baseFee.
        """
        if (
            self.upperLimitForBaseFeeInGwei is not None
            and gasFeeInGwei > self.upperLimitForBaseFeeInGwei
        ):
            raise TransactionTooExpensive(
                f"Gas too expensive [fee={gasFeeInGwei} gwei, max={self.upperLimitForBaseFeeInGwei} gwei]"
            )

    ####################
    # Utils
    ####################

    def getNonce(self, address: Address = None) -> Nonce:
        if not address:
            address = self.userAddress
        return self.w3.eth.get_transaction_count(address)

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

    def estimateGasForTransfer(self, to: Address, valueInWei: Wei) -> int:
        """
        Return the gas that would be required to send some ETH
        (expressed in Wei) to an address
        """
        return self.w3.eth.estimate_gas(
            {
                "from": self.userAddress,
                "to": to,
                "value": valueInWei,
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

    @staticmethod
    def getGasSpentInEth(txReceipt: TxReceipt) -> float:
        """
        Given the transaction receipt, return the ETH that
        was spent in gas to process the transaction
        """
        return float(
            Web3.fromWei(txReceipt["effectiveGasPrice"] * txReceipt["gasUsed"], "ether")
        )
