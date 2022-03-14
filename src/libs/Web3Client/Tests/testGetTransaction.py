from typing import cast
from src.libs.Web3Client.helpers.debug import pprintAttributeDict
from src.helpers.general import secondOrNone
from src.common.config import nodeUri
from src.libs.Web3Client.Web3Client import Web3Client
from sys import argv
from eth_typing.encoding import HexStr

# VARS
txHash = cast(
    HexStr,
    (
        secondOrNone(argv)
        or "0xc333db84c2c5d114f8168d92b9114c6325ae541f2758a5ae539055539721d00c"
    ),
)

client = Web3Client().setNodeUri(nodeUri)
txReceipt = client.getTransactionReceipt(txHash)
tx = client.getTransaction(txHash)

# TEST FUNCTIONS
def testGetTransaction() -> None:
    print(">>> TX RECEIPT")
    pprintAttributeDict(txReceipt)
    print(">>> ACTUAL TX")
    pprintAttributeDict(tx)


# EXECUTE
testGetTransaction()
