"""
Extract event log from a startGame contract transaction; the event
is called gameStarted and should be defined in the contract's ABI.

Docs: https://web3py.readthedocs.io/en/stable/contracts.html#events
"""

from typing import cast
from src.libs.Web3Client.helpers.debug import pprintAttributeDict
from src.helpers.general import secondOrNone
from src.common.config import nodeUri
from src.libs.CrabadaWeb3Client.CrabadaWeb3Client import CrabadaWeb3Client
from sys import argv
from eth_typing.encoding import HexStr
from pprint import pprint

# VARS
txHash = cast(
    HexStr,
    (
        secondOrNone(argv)
        or "0x41705baf18b1ebc8ec204926a8524d3530aada11bd3c249ca4a330ed047f005e"
    ),
)

client = CrabadaWeb3Client(nodeUri=nodeUri)

tx = client.getTransaction(txHash)
txReceipt = client.getTransactionReceipt(txHash)
logs = client.contract.events.StartGame().processReceipt(txReceipt)

# TEST FUNCTIONS
def test() -> None:
    print(">>> TX")
    pprint(tx)
    print(">>> TX LOGS")
    for log in logs:
        pprintAttributeDict(log)


# EXECUTE
test()
