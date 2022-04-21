from typing import cast
from src.common.types import Tus
from src.helpers.general import fourthOrNone, nthOrNone, secondOrNone, thirdOrNone
from src.helpers.reinforce import minerCanReinforce
from src.models.User import User
from src.strategies.reinforce.ReinforceStrategyFactory import (
    makeReinforceStrategy,
)
from src.common.clients import makeCrabadaWeb2Client
from sys import argv

# VARS
user = User.find(1)
teamConfig = user.getTeams()[0]

maxPrice = cast(
    Tus, int(secondOrNone(argv) or user.config["reinforcementMaxPriceInTus"])
)
reinforcementToPick = int(thirdOrNone(argv) or teamConfig["reinforcementToPick"])
strategyName = fourthOrNone(argv) or teamConfig["reinforceStrategies"][0]

# Get the first mine that can be reinforced
openMines = makeCrabadaWeb2Client().listOpenMines({"limit": 100})
reinforceableMines = [m for m in openMines if minerCanReinforce(m)]
game = secondOrNone(reinforceableMines)

if not game:
    print("Could not find a reinforceable mine, try after a few seconds")
    exit(1)

# Override config with CLI arguments
teamConfig["reinforcementToPick"] = reinforcementToPick

# TEST FUNCTIONS
def test() -> None:
    strategy = makeReinforceStrategy(strategyName, user, teamConfig, game, maxPrice)
    print(">>> CHOSEN REINFORCE STRATEGY")
    try:
        print(strategy.__class__.__name__)
    except Exception as e:
        print("ERROR RAISED: " + e.__class__.__name__ + ": " + str(e))
    print(">>> REINFORCEMENT_TO_PICK SETTING")
    print(f"{reinforcementToPick}")
    print(">>> REINFORCEMENT CRAB")
    try:
        print(strategy.getCrab("MINING"))
    except Exception as e:
        print("ERROR RAISED: " + e.__class__.__name__ + ": " + str(e))


# EXECUTE
test()
