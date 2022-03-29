from src.helpers import mines, reinforce
from src.helpers.general import secondOrNone
from src.common.clients import crabadaWeb2Client
from sys import argv
from pprint import pprint

# VARS
mineId = secondOrNone(argv) or 269751
mine = crabadaWeb2Client.getMine(mineId)

# TEST FUNCTIONS
def test() -> None:
    print(">>> MINE'S PROCESS")
    pprint(mine["process"])
    print("")
    print(">>> GENERAL")
    print(f"mineIsOpen = {mines.mineIsOpen(mine)}")
    print(f"mineIsClosed = {mines.mineIsClosed(mine)}")
    print(f"mineIsFinished = {mines.mineIsFinished(mine)}")
    print("")
    print(">>> TIME RELATED")
    print(f"getElapsedTime = {mines.getElapsedTime(mine)}"),
    print(f"getElapsedTimeFormatted = {mines.getElapsedTimeFormatted(mine)}"),
    print(f"getRemainingTime = {mines.getRemainingTime(mine)}"),
    print(f"getRemainingTimeFormatted = {mines.getRemainingTimeFormatted(mine)}"),
    print(f"getLastAction = {mines.getLastAction(mine)}"),
    print(
        f"getElapsedTimeSinceLastAction = {mines.getElapsedTimeSinceLastAction(mine)}"
    ),
    print("")
    print(">>> ATTACK RELATED")
    print(f"mineHasBeenAttacked = {mines.mineHasBeenAttacked(mine)}"),
    print(f"attackIsOver = {mines.attackIsOver(mine)}"),
    print(f"mineIsSettled = {mines.mineIsSettled(mine)}"),
    print(f"mineCanBeSettled = {mines.mineCanBeSettled(mine)}"),
    print(f"mineIsWaitToSettle = {mines.mineIsWaitToSettle(mine)}"),
    print(f"getTimesMinerReinforced = {mines.getTimesMinerReinforced(mine)}"),
    print(f"getTimesLooterReinforced = {mines.getTimesLooterReinforced(mine)}"),
    print(f"getRemainingTimeBeforeSettle = {mines.getRemainingTimeBeforeSettle(mine)}"),
    print(
        f"getRemainingTimeBeforeSettleFormatted = {mines.getRemainingTimeBeforeSettleFormatted(mine)}"
    ),
    print(
        f"getMinerReinforcementStatus = {reinforce.getMinerReinforcementStatus(mine)}"
    ),
    print(
        f"getLooterReinforcementStatus = {reinforce.getLooterReinforcementStatus(mine)}"
    ),


# EXECUTE
test()
