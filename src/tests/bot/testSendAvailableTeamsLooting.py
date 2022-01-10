from src.bot.sendTeams import sendAvailableTeamsLooting
from src.common.config import users

# VARS

# TEST FUNCTIONS
def testSendAvailableTeamsLooting() -> None:
    nSent = sendAvailableTeamsLooting(users[0]['address'])
    print(f'SENT {nSent} TEAMS LOOTING')

# EXECUTE
testSendAvailableTeamsLooting()