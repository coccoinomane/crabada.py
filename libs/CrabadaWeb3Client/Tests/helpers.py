from pprint import pprint

def printTxInfo(client, txHash):
    print(">>> TX SENT!")
    print("Hash = " + txHash)
    print("Waiting for transaction to finalize...")
    tx_receipt = client.w3.eth.wait_for_transaction_receipt(txHash)
    print(">>> TX IS ON THE BLOCKCHAIN :-)")
    pprint(tx_receipt)
    print(">>> ETH SPENT")
    print(client.w3.fromWei(tx_receipt['effectiveGasPrice']*tx_receipt['gasUsed'], 'ether'))
