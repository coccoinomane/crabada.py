from src.helpers import Mines
from src.helpers.General import secondOrNone
from src.common.clients import crabadaWeb2Client
from sys import argv
from pprint import pprint

# VARS
mineId = secondOrNone(argv) or 269751
mine = crabadaWeb2Client.getMine(mineId)

# TEST FUNCTIONS
def testMineStatus() -> None:
    output = {
        'mineHasBeenAttacked': Mines.mineHasBeenAttacked(mine),
        'mineIsOpen': Mines.mineIsOpen(mine),
        'mineIsSettled': Mines.mineIsSettled(mine),
        'mineIsFinished': Mines.mineIsFinished(mine),
        'mineIsClosed': Mines.mineIsClosed(mine),
        'getRemainingTime': Mines.getRemainingTime(mine),
        'getRemainingTimeFormatted': Mines.getRemainingTimeFormatted(mine),
        'getNextMineToFinish': Mines.getNextMineToFinish([mine]),
    }
    pprint(output)

# EXECUTE
testMineStatus()