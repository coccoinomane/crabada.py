from src.helpers.Games import closeFinishedGames
from src.common.config import users

# VARS

# TEST FUNCTIONS
def testCloseFinishedGames() -> None:
    nFinished = closeFinishedGames(users[0]['address'])
    print(f'CLOSED {nFinished} GAMES')

# EXECUTE
testCloseFinishedGames()