"""
Extract event log from a contract transaction; you need to
replace myEvent() with the event name, which should be defined in
the contract's ABI.

Docs: https://web3py.readthedocs.io/en/stable/contracts.html#events
"""

from typing import cast
from src.libs.Web3Client.helpers.debug import printTxInfo
from src.helpers.general import secondOrNone
from src.common.config import nodeUri, users, contract, chainId
from src.libs.CrabadaWeb3Client.CrabadaWeb3Client import CrabadaWeb3Client
from sys import argv
from eth_typing.encoding import HexStr
from pprint import pprint
from web3 import Web3

# VARS
txHash = cast(HexStr, (secondOrNone(argv) or "0xc333db84c2c5d114f8168d92b9114c6325ae541f2758a5ae539055539721d00c"))

client = cast(CrabadaWeb3Client, (CrabadaWeb3Client()
    .setNodeUri(nodeUri)
    .setContract(contract['address'], contract['abi'])
    .setChainId(chainId)))

tx = client.getTransaction(txHash)
txReceipt = client.getTransactionReceipt(txHash)
logs = client.contract.events.myEvent().processReceipt(txReceipt)

# TEST FUNCTIONS
def testContractEvents() -> None:
    print(">>> TX")
    pprint(tx)
    print(">>> TX LOGS")
    pprint(logs)

# EXECUTE
testContractEvents()