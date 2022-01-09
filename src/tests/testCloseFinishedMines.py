from src.helpers.Games import closeFinishedMines
from src.common.config import users

# VARS

# TEST FUNCTIONS
def testcloseFinishedMines() -> None:
    nFinished = closeFinishedMines(users[0]['address'])
    print(f'CLOSED {nFinished} LOOTING MINES')

# EXECUTE
testcloseFinishedMines()