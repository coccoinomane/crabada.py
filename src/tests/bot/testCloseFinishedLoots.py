from src.bot.closeMines import closeFinishedLoots
from src.common.config import users

# VARS

# TEST FUNCTIONS
def testcloseFinishedLoots() -> None:
    nFinished = closeFinishedLoots(users[0]['address'])
    print(f'CLOSED {nFinished} LOOTING GAMES')

# EXECUTE
testcloseFinishedLoots()