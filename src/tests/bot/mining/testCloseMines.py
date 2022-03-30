from src.bot.mining.closeMines import closeMines
from src.common.config import users
from src.models.User import User

# VARS

# TEST FUNCTIONS
def testCloseMines() -> None:
    nFinished = closeMines(User(users[0]["address"]))
    print(f"CLOSED {nFinished} LOOTING MINES")


# EXECUTE
testCloseMines()
