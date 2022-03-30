from src.bot.looting.closeLoots import closeLoots
from src.common.config import users
from src.models.User import User

# VARS

# TEST FUNCTIONS
def testCloseLoots() -> None:
    nFinished = closeLoots(User(users[0]["address"]))
    print(f"CLOSED {nFinished} LOOTING GAMES")


# EXECUTE
testCloseLoots()
