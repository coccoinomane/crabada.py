"""
Use the "make" functions defined in this class to dinamically
instantiate strategies.

Also provides utility function to easily return products of
strategies (mine, crab, etc) without having to type boilerplate.
"""

from src.common.exceptions import StrategyException, StrategyNotFound, StrategyNotSet
from src.common.clients import crabadaWeb2Client
from src.common.types import ConfigTeam
from src.libs.CrabadaWeb2Client.types import Game, Team
from src.strategies.loot.LootStrategy import LootStrategy
from src.strategies.loot.LowestBp import LowestBp
from src.models.User import User

lootStrategies = {
    "LowestBp": LowestBp,
}


def getBestMineToLoot(user: User, team: Team) -> Game:
    """
    Find best mine to loot for the given team, using the Loot strategy
    provided in the user settings
    """

    # Fetch the strategy name from the user settings
    teamConfig = User(user.address).getTeamConfig(team["team_id"])
    strategyName = teamConfig.get("lootStrategyName")
    if not strategyName:
        raise StrategyNotSet(f"Team {teamConfig['id']} has no loot strategy set")

    # Create the strategy object and use it to get the mine
    strategy: LootStrategy = makeLootStrategy(strategyName, user, teamConfig, team)

    return strategy.getMine()


def makeLootStrategy(
    strategyName: str, user: User, teamConfig: ConfigTeam, team: Team
) -> LootStrategy:
    """
    Instantiate and return the Loot Strategy with the given name
    and the given parameters
    """
    strategyClass = lootStrategies.get(strategyName)
    if not strategyClass:
        raise StrategyNotFound(f"Cound not find a lootStrategy named {strategyName}")
    if not issubclass(strategyClass, (LootStrategy)):
        raise StrategyException(f"Error fetching loot strategy {strategyName}")

    return strategyClass(user, teamConfig, crabadaWeb2Client).setParams(team)
