from src.libs.Web3Watcher.Watcher import Watcher
from src.common.config import nodeUri
from src.libs.Web3Client.AvalancheCWeb3Client import AvalancheCWeb3Client
from src.helpers.general import secondOrNone
from sys import argv

# VARS
pollInterval = float(secondOrNone(argv) or 2)  # seconds
doAsync = False
handler = lambda log: print(log)

# TEST FUNCTIONS
def testWatchLatestBlock() -> None:
    client = AvalancheCWeb3Client().setNodeUri(nodeUri)
    watcher = Watcher(client, doAsync).setFilterParams("latest")
    watcher.addHandler(lambda log: print(log))
    watcher.run(pollInterval)


# EXECUTE
testWatchLatestBlock()
