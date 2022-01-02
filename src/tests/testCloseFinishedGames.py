from src.helpers.Games import closeFinishedGames
from src.common.config import users

# VARS

# TEST FUNCTIONS
def testCloseFinishedGames() -> None:
    closeFinishedGames(users[0]['address'])

# EXECUTE
testCloseFinishedGames()