from src.bot.looting.reinforceAttack import reinforceAttack
from src.common.config import users

# VARS

# TEST FUNCTIONS
def testReinforceAttack() -> None:
    nBorrowed = reinforceAttack(users[0]["address"])
    print(f"BORROWED {nBorrowed} REINFORCEMENT")


# EXECUTE
testReinforceAttack()
