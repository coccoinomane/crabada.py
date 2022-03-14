from typing import cast
from src.libs.Web3Watcher.Watcher import Watcher
from web3.types import FilterParams
from src.common.config import nodeUri, users
from src.libs.CrabadaWeb3Client.CrabadaWeb3Client import CrabadaWeb3Client
from src.helpers.general import secondOrNone
from src.libs.Web3Client.helpers.debug import pprintAttributeDict
from pprint import pprint
from sys import argv

# VARS
client = cast(CrabadaWeb3Client, (CrabadaWeb3Client().setNodeUri(nodeUri)))
event = client.contract.events.StartGame()
filter = event.createFilter(fromBlock="latest")

pollInterval = float(secondOrNone(argv) or 2)  # seconds
doAsync = True
handler = lambda log: print(log)

# TEST FUNCTIONS
def testWatchCrabadaEvent() -> None:
    watcher = Watcher(client, doAsync).setFilter(filter)
    watcher.addHandler(lambda log: pprintAttributeDict(log))
    watcher.addNotFoundHandler(lambda: print("No event found"))
    watcher.run(pollInterval)


# EXECUTE
testWatchCrabadaEvent()
