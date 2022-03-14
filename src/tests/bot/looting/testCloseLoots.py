from src.bot.looting.closeLoots import closeLoots
from src.common.config import users

# VARS

# TEST FUNCTIONS
def testCloseLoots() -> None:
    nFinished = closeLoots(users[0]["address"])
    print(f"CLOSED {nFinished} LOOTING GAMES")


# EXECUTE
testCloseLoots()
