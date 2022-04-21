from src.common.config import users, donatePercentage, nodeUri, notifications, telegram
from pprint import pprint

# VARS

# TEST FUNCTIONS
def test() -> None:
    pprint(">>> USERS & TEAMS")
    for user in users:
        del user["privateKey"]  # type: ignore
    pprint(users)
    print(">>> NODE URI")
    print(nodeUri)
    print(">>> DONATE PERCENT")
    print(donatePercentage)
    print(">>> NOTIFICATIONS")
    print(notifications)
    print(">>> TELEGRAM")
    print(telegram)


# EXECUTE
test()
