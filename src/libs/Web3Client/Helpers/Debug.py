from eth_typing.encoding import HexStr
from src.libs.Web3Client.Web3Client import Web3Client
from web3 import Web3
from pprint import pprint

def printTxInfo(client: Web3Client, txHash: HexStr) -> None:
    """Get a transaction receipt and print it, together with
    the tx cost"""
    print(">>> TX SENT!")
    print("Hash = " + txHash)
    print("Waiting for transaction to finalize...")
    tx_receipt = client.w3.eth.wait_for_transaction_receipt(txHash)
    print(">>> TX IS ON THE BLOCKCHAIN :-)")
    pprint(tx_receipt)
    print(">>> ETH SPENT")
    print(Web3.fromWei(tx_receipt['effectiveGasPrice']*tx_receipt['gasUsed'], 'ether'))
