from src.common.config import users
from src.helpers.mines import fetchOpenMines
from src.models.User import User

# VARS

# TEST FUNCTIONS
def testFetchOpenMines() -> None:
    openMines = fetchOpenMines(User(users[0]["address"]))
    print(openMines)


# EXECUTE
testFetchOpenMines()
