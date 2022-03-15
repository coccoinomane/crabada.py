from src.bot.mining.reinforceDefense import reinforceDefense
from src.common.config import users

# VARS

# TEST FUNCTIONS
def testReinforceDefense() -> None:
    nBorrowed = reinforceDefense(users[0]["address"])
    print(f"BORROWED {nBorrowed} REINFORCEMENT")


# EXECUTE
testReinforceDefense()
