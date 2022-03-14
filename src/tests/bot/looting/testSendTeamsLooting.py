from src.bot.looting.sendTeamsLooting import sendTeamsLooting
from src.common.config import users

# VARS

# TEST FUNCTIONS
def testSendTeamsLooting() -> None:
    nSent = sendTeamsLooting(users[0]["address"])
    print(f"SENT {nSent} TEAMS LOOTING")


# EXECUTE
testSendTeamsLooting()
