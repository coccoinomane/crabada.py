from pprint import pprint
from typing import cast
from src.common.types import Tus
from src.helpers.general import secondOrNone
from src.helpers.reinforce import minerCanReinforce
from src.strategies.StrategyFactory import makeReinforceStrategy
from src.common.clients import crabadaWeb2Client
from src.common.config import users
from sys import argv

# VARS
maxPrice = cast(Tus, int(secondOrNone(argv) or 25))

# Get the first mine that can be reinforced
openMines = crabadaWeb2Client.listOpenMines({"limit": 100})
reinforceableMines = [m for m in openMines if minerCanReinforce(m)]
game = secondOrNone(reinforceableMines)

if not game:
    print("Could not find a reinforceable mine, try after a few seconds")
    exit(1)

userAddress = users[0]["address"]
teamConfig = users[0]["teams"][0]
strategyName = teamConfig.get("reinforceStrategyName")

# TEST FUNCTIONS
def testMakeReinforceStrategy() -> None:
    strategy = makeReinforceStrategy(strategyName, game, maxPrice)
    print(">>> REINFORCE STRATEGY FROM .ENV")
    print(strategyName)
    print(">>> ACTUAL REINFORCE STRATEGY THAT WILL BE USED")
    try:
        print(strategy.__class__.__name__)
    except Exception as e:
        print("ERROR RAISED: " + e.__class__.__name__ + ": " + str(e))
    print(">>> REINFORCEMENT CRAB")
    try:
        print(
            strategy.getCrab("MINING")
        )  # Will print note if mine is not reinforceable
    except Exception as e:
        print("ERROR RAISED: " + e.__class__.__name__ + ": " + str(e))


# EXECUTE
testMakeReinforceStrategy()
