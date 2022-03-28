from src.helpers import mines
from src.helpers.general import secondOrNone
from src.common.clients import crabadaWeb2Client
from sys import argv
from pprint import pprint

# VARS
mineId = secondOrNone(argv) or 269751
mine = crabadaWeb2Client.getMine(mineId)

# TEST FUNCTIONS
def testMineStatus() -> None:
    output = {
        "mineHasBeenAttacked": mines.mineHasBeenAttacked(mine),
        "mineIsOpen": mines.mineIsOpen(mine),
        "mineReadyToBeSettled": mines.mineReadyToBeSettled(mine),
        "mineIsFinished": mines.mineIsFinished(mine),
        "mineIsClosed": mines.mineIsClosed(mine),
        "getRemainingTime": mines.getRemainingTime(mine),
        "getRemainingTimeFormatted": mines.getRemainingTimeFormatted(mine),
        "getNextMineToFinish": mines.getNextMineToFinish([mine]),
    }
    pprint(output)


# EXECUTE
testMineStatus()
