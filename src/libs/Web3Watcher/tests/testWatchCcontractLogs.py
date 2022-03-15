"""
Watch all logs from the given contract (default: Crabada game
contract) with the given polling interval (default: 2 seconds).
"""
from typing import cast
from src.libs.Web3Client.Web3Client import Web3Client
from src.libs.Web3Watcher.Watcher import Watcher
from web3.types import FilterParams
from src.common.config import nodeUri, users
from src.libs.CrabadaWeb3Client.CrabadaWeb3Client import CrabadaWeb3Client
from src.helpers.general import secondOrNone, thirdOrNone
from src.libs.Web3Client.helpers.debug import pprintAttributeDict
from sys import argv
from web3 import Web3

# VARS
contractAddress = Web3.toChecksumAddress(
    secondOrNone(argv) or CrabadaWeb3Client.contractAddress
)
pollInterval = float(thirdOrNone(argv) or 2)  # seconds

client = Web3Client().setNodeUri(nodeUri)

filterParams: FilterParams = {
    "fromBlock": "latest",
    "address": contractAddress,
}

doAsync = True
handler = lambda log: print(log)

# TEST FUNCTIONS
def testWatchContractLogs() -> None:
    watcher = Watcher(client, doAsync).setFilterParams(filterParams)
    watcher.addHandler(lambda log: pprintAttributeDict(log))
    watcher.addNotFoundHandler(lambda: print("No event found"))
    watcher.run(pollInterval)


# EXECUTE
testWatchContractLogs()
