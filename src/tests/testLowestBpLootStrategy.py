from typing import cast
from src.common.types import Tus
from src.common.config import users
from src.helpers.General import firstOrNone, secondOrNone, thirdOrNone
from src.strategies.loot.LowestBpStrategy import LowestBpStrategy
from src.common.clients import crabadaWeb2Client
from pprint import pprint

# VARS
userAddress = users[0]['address']
teamId = users[0]['teams'][0]['id']
teams = crabadaWeb2Client.listTeams(userAddress)
team = firstOrNone([ t for t in teams if t['team_id'] == teamId ])

if not team:
    print('Error getting team with ID ' + str(teamId))
    exit(1)

strategy: LowestBpStrategy = LowestBpStrategy(crabadaWeb2Client).setParams(team)

# TEST FUNCTIONS
def testLowestBpStrategy() -> None:

    print('>>> IS STRATEGY APPLICABLE?')
    print(strategy.isApplicable())

    print('>>> CHOSEN MINE')
    try:
        print(strategy.getMine())
    except Exception as e:
        print('ERROR RAISED: ' + e.__class__.__name__ + ': ' + str(e))

# EXECUTE
testLowestBpStrategy()