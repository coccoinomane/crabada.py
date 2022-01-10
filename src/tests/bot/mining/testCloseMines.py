from src.bot.mining.closeMines import closeMines
from src.common.config import users

# VARS

# TEST FUNCTIONS
def testCloseMines() -> None:
    nFinished = closeMines(users[0]['address'])
    print(f'CLOSED {nFinished} LOOTING MINES')

# EXECUTE
testCloseMines()