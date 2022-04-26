"""
Extract event logs from a closeGame contract transaction.

There should be three logs:
- CloseGame event
- Transfer TUS event
- Transfer CRA event

Example: 
https://snowtrace.io/tx/0x143fbb963df559bacb1245a39ad586da80b68629906792e928787f467fa09ed8#eventlog

Docs:
https://web3py.readthedocs.io/en/stable/contracts.html#events
"""

from typing import cast

from eth_typing import Address
from src.libs.Web3Client.helpers.debug import pprintAttributeDict
from src.helpers.general import secondOrNone
from src.common.config import nodeUri
from src.libs.CrabadaWeb3Client.CrabadaWeb3Client import CrabadaWeb3Client
from src.libs.Web3Client.Web3ClientFactory import makeErc20Client
from sys import argv
from eth_typing.encoding import HexStr
from pprint import pprint

# VARS
txHash = cast(
    HexStr,
    (
        secondOrNone(argv)
        or "0x143fbb963df559bacb1245a39ad586da80b68629906792e928787f467fa09ed8"
    ),
)

crabadaClient = CrabadaWeb3Client(nodeUri=nodeUri)
erc20Client = makeErc20Client(
    "Avalanche", nodeUri, cast(Address, "0x0000000000000000000000000000000000000000")
)

txReceipt = crabadaClient.getTransactionReceipt(txHash)
closeGameLog = crabadaClient.contract.events.CloseGame().processReceipt(txReceipt)
transferLogs = erc20Client.contract.events.Transfer().processReceipt(txReceipt)

# TEST FUNCTIONS
def test() -> None:
    print(">>> TX RECEIPT")
    pprint(txReceipt)
    print(">>> CLOSE GAME LOG")
    for log in closeGameLog:
        pprintAttributeDict(log)
    print(">>> TRANSFER LOGS")
    for log in transferLogs:
        pprintAttributeDict(log)


# EXECUTE
test()
