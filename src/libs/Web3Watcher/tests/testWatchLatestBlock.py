from src.libs.Web3Watcher.Watcher import Watcher
from src.common.config import nodeUri
from pprint import pprint
from src.libs.Web3Client.AvalancheCWeb3Client import AvalancheCWeb3Client
from src.libs.Web3Client.helpers.debug import pprintAttributeDict

# VARS
pollInterval = 2 # seconds
client = AvalancheCWeb3Client().setNodeUri(nodeUri)
watcher = Watcher(client).setFilterParams('latest')
watcher.addHandler(lambda log: print(log))

# TEST FUNCTIONS
def testWatchLatestBlock() -> None:
    watcher.run(pollInterval)

# EXECUTE
testWatchLatestBlock()