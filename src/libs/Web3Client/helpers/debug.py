from typing import Any, Union
from eth_typing.encoding import HexStr
from src.common.logger import formatAttributeDict
from src.libs.Web3Client.Web3Client import Web3Client
from web3.datastructures import AttributeDict
from web3.types import TxReceipt
import pprint


def printTxInfo(client: Web3Client, txHash: HexStr) -> None:
    """
    Get a transaction receipt and print it, together with
    the tx cost
    """
    print(">>> TX SENT!")
    print("Hash = " + txHash)
    print("Waiting for transaction to finalize...")
    tx_receipt = client.getTransactionReceipt(txHash)
    print(">>> TX IS ON THE BLOCKCHAIN :-)")
    pprint.pprint(tx_receipt)
    print(">>> ETH SPENT")
    print(Web3Client.getGasSpentInEth(tx_receipt))


def pprintAttributeDict(
    attributeDict: Union[TxReceipt, AttributeDict[str, Any]]
) -> None:
    """
    Web3 often returns AttributeDict instead of simple Dictionaries;
    this function pretty prints an AttributeDict
    """
    print(formatAttributeDict(attributeDict))
