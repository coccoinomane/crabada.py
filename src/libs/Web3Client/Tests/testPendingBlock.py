"""
Check whether the pending block is any different than
the latest block.

If they are identical, it might mean that the RPC does
not support pending transactions (e.g. because it is not
a full validator node).
"""
from src.common.config import nodeUri, users
from src.libs.Web3Client.AvalancheCWeb3Client import AvalancheCWeb3Client
import pprint

from src.libs.Web3Client.helpers.debug import pprintAttributeDict

# VARS
client = (
    AvalancheCWeb3Client().setNodeUri(nodeUri).setCredentials(users[0]["privateKey"])
)

latest = client.w3.eth.get_block("latest")
pending = client.w3.eth.get_block("pending")

# TEST FUNCTIONS
def testPendingBlock() -> None:
    diffBlock = {}
    for key in pending:
        diffBlock[key] = "equal" if latest[key] == pending[key] else "different"  # type: ignore
    print(">>> EQUAL VALUES")
    for key, value in diffBlock.items():
        if value == "equal":
            print(f"  > Key '{key}' is equal with value {pprint.pformat(latest[key], indent=6)}")  # type: ignore
    print(">>> DIFFERENT VALUES")
    for key, value in diffBlock.items():
        if value == "different":
            print(f"  > Key '{key}' is different")
            print(f"    value latest  = {pprint.pformat(latest[key], indent=8)}")  # type: ignore
            print(f"    value pending = {pprint.pformat(pending[key], indent=8)}")  # type: ignore


# EXECUTE
testPendingBlock()
