from typing import cast
from src.common.types import Tus
from src.helpers.general import secondOrNone, thirdOrNone
from src.strategies.StrategyFactory import getBestReinforcement, makeReinforceStrategy
from src.common.clients import crabadaWeb2Client
from src.common.config import users
from sys import argv

# VARS
gameId = int(secondOrNone(argv)) or 2421165
maxPrice = cast(Tus, int(thirdOrNone(argv) or 25))

game = crabadaWeb2Client.getMine(gameId)

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
