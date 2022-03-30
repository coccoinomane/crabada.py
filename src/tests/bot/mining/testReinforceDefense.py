from src.bot.mining.reinforceDefense import reinforceDefense
from src.common.config import users
from src.models.User import User

# VARS

# TEST FUNCTIONS
def testReinforceDefense() -> None:
    nBorrowed = reinforceDefense(User(users[0]["address"]))
    print(f"BORROWED {nBorrowed} REINFORCEMENT")


# EXECUTE
testReinforceDefense()
