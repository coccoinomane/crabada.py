from src.bot.looting.reinforceAttack import reinforceAttack
from src.common.config import users
from src.models.User import User

# VARS

# TEST FUNCTIONS
def testReinforceAttack() -> None:
    nBorrowed = reinforceAttack(User(users[0]["address"]))
    print(f"BORROWED {nBorrowed} REINFORCEMENT")


# EXECUTE
testReinforceAttack()
