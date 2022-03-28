from sys import argv
from src.common.config import users
from src.helpers.general import secondOrNone
from src.helpers.mines import fetchOpenLoots
from src.models.User import User

# VARS
userNumber = int(secondOrNone(argv) or 1)

# TEST FUNCTIONS
def test() -> None:
    openLoots = fetchOpenLoots(User.find(userNumber))
    print(openLoots)


# EXECUTE
test()
