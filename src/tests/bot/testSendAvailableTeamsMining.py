from src.bot.sendTeams import sendAvailableTeamsMining
from src.common.config import users

# VARS

# TEST FUNCTIONS
def testSendAvailableTeamsMining() -> None:
    nSent = sendAvailableTeamsMining(users[0]['address'])
    print(f'SENT {nSent} TEAMS MINING')

# EXECUTE
testSendAvailableTeamsMining()