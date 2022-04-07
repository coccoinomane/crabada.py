from src.common.config import users, donatePercentage, nodeUri
from pprint import pprint

# VARS

# TEST FUNCTIONS
def test() -> None:
    pprint(">>> USERS & TEAMS")
    pprint(users)
    print(">>> NODE URI")
    print(nodeUri)
    print(">>> DONATE PERCENT")
    print(donatePercentage)


# EXECUTE
test()
