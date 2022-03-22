from pprint import pprint
from typing import cast
from src.common.types import Tus
from src.helpers.general import secondOrNone, thirdOrNone
from src.helpers.reinforce import minerCanReinforce
from src.models.User import User
from src.strategies.reinforce.ReinforceStrategyFactory import makeReinforceStrategy
from src.common.clients import crabadaWeb2Client
from src.common.config import users
from sys import argv

# VARS
maxPrice = cast(Tus, int(secondOrNone(argv) or 25))
reinforcementToPick = int(thirdOrNone(argv) or 0)

# Get the first mine that can be reinforced
openMines = crabadaWeb2Client.listOpenMines({"limit": 100})
reinforceableMines = [m for m in openMines if minerCanReinforce(m)]
game = secondOrNone(reinforceableMines)

if not game:
    print("Could not find a reinforceable mine, try after a few seconds")
    exit(1)

user = User(users[0]["address"])
teamConfig = users[0]["teams"][0]
if reinforcementToPick:  # override team config for faster testing
    teamConfig["reinforcementToPick"] = reinforcementToPick
strategyName = teamConfig.get("reinforceStrategyName")

# TEST FUNCTIONS
def testMakeReinforceStrategy() -> None:
    strategy = makeReinforceStrategy(strategyName, user, teamConfig, game, maxPrice)
    print(">>> REINFORCE STRATEGY FROM .ENV")
    print(strategyName)
    print(">>> ACTUAL REINFORCE STRATEGY THAT WILL BE USED")
    try:
        print(strategy.__class__.__name__)
    except Exception as e:
        print("ERROR RAISED: " + e.__class__.__name__ + ": " + str(e))
    print(">>> REINFORCEMENT CRAB THAT WILL BE PICKED")
    print(reinforcementToPick)
    print(">>> REINFORCEMENT CRAB")
    try:
        print(strategy.getCrab("MINING"))
    except Exception as e:
        print("ERROR RAISED: " + e.__class__.__name__ + ": " + str(e))


# EXECUTE
testMakeReinforceStrategy()
