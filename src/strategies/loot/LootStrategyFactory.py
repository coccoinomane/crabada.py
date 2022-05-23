"""
Use the "make" function defined in this class to dinamically
instantiate strategies.

Also provides utility function to easily return products of
strategies (mine, crab, etc) without having to type boilerplate.
"""

from src.common.exceptions import (
    NoSuitableMineFound,
    StrategyException,
    StrategyNotFound,
    StrategyNotSet,
)
from src.common.clients import makeIdleGameWeb2Client
from src.common.types import ConfigTeam
from src.libs.CrabadaWeb2Client.types.idleGameTypes import Game, Team
from src.strategies.loot.LootStrategy import LootStrategy
from src.strategies.loot.LowestBp import LowestBp
from src.models.User import User

lootStrategies = {
    "LowestBp": LowestBp,
}


def getBestMineToLoot(user: User, team: Team) -> Game:
    """
    Find best mine to loot for the given team, using the first suitable
    Loot strategy provided in the user settings
    """
    teamConfig = user.getTeamConfig(team["team_id"])

    mine: Game = None

    for strategyName in teamConfig["lootStrategies"]:
        strategy: LootStrategy = makeLootStrategy(strategyName, user, teamConfig, team)
        mine = strategy.getMine()
        if mine:
            return mine

    raise NoSuitableMineFound(
        f"No suitable mine to loot found [team={teamConfig['id']}]"
    )


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

    return strategyClass(user, teamConfig, makeIdleGameWeb2Client()).setParams(team)
