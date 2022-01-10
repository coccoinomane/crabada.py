from src.bot.reinforce import reinforceWhereNeeded
from src.common.config import users

# VARS

# TEST FUNCTIONS
def testReinforceWhereNeeded() -> None:
    nBorrowed = reinforceWhereNeeded(users[0]['address'])
    print(f'BORROWED {nBorrowed} REINFORCEMENT')

# EXECUTE
testReinforceWhereNeeded()