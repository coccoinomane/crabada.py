from src.bot.mining.sendTeamsMining import sendTeamsMining
from src.common.config import users
from src.models.User import User

# VARS

# TEST FUNCTIONS
def testSendTeamsMining() -> None:
    nSent = sendTeamsMining(User(users[0]["address"]))
    print(f"SENT {nSent} TEAMS MINING")


# EXECUTE
testSendTeamsMining()
