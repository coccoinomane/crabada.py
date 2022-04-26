from typing import cast
from src.common.types import Tus
from src.helpers.general import fourthOrNone, secondOrNone, thirdOrNone
from src.helpers.reinforce import minerCanReinforce
from src.models.User import User
from src.strategies.reinforce.ReinforceStrategyFactory import (
    getBestReinforcement,
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
reinforceStrategies = teamConfig["reinforceStrategies"]
if fourthOrNone(argv):
    reinforceStrategies = [x.strip() for x in fourthOrNone(argv).split(",")]

# Get the first mine that can be reinforced
openMines = makeCrabadaWeb2Client().listOpenMines({"limit": 100})
reinforceableMines = [m for m in openMines if minerCanReinforce(m)]
game = secondOrNone(reinforceableMines)

if not game:
    print("Could not find a reinforceable mine, try after a few seconds")
    exit(1)

# Override config with CLI arguments
teamConfig["reinforcementToPick"] = reinforcementToPick
teamConfig["reinforceStrategies"] = reinforceStrategies

# TEST FUNCTIONS
def test() -> None:
    print(">>> CHOSEN REINFORCE STRATEGIES")
    print(teamConfig["reinforceStrategies"])
    print(">>> REINFORCEMENT CRAB THAT WILL BE PICKED")
    print(reinforcementToPick)
    print(">>> REINFORCEMENT CRAB")
    print(getBestReinforcement(user, game, maxPrice, teamConfig, "MINING"))


# EXECUTE
test()
