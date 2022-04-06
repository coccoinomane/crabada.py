from sys import argv
from src.common.config import users
from src.helpers.general import secondOrNone
from src.helpers.mines import fetchOpenMines
from src.models.User import User

# VARS
userNumber = int(secondOrNone(argv) or 1)

# TEST FUNCTIONS
def test() -> None:
    openMines = fetchOpenMines(User.find(userNumber))
    print(openMines)


# EXECUTE
test()
