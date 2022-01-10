from src.bot.mining.sendTeamsMining import sendTeamsMining
from src.common.config import users

# VARS

# TEST FUNCTIONS
def testSendTeamsMining() -> None:
    nSent = sendTeamsMining(users[0]['address'])
    print(f'SENT {nSent} TEAMS MINING')

# EXECUTE
testSendTeamsMining()