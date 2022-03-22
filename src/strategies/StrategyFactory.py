"""
Use the "make" functions defined in this class to dinamically
instantiate strategies.

Also provides utility function to easily return products of
strategies (mine, crab, etc) without having to type boilerplate.
"""

from typing import Any
from eth_typing.evm import Address
from src.common.exceptions import StrategyException, StrategyNotFound, StrategyNotSet
from src.common.clients import crabadaWeb2Client
from src.common.types import ConfigTeam, ConfigUser, Tus
from src.libs.CrabadaWeb2Client.types import CrabForLending, Game, Team
from src.strategies.loot.LootStrategy import LootStrategy
from src.strategies.loot.LowestBpLootStrategy import LowestBpLootStrategy
from src.strategies.reinforce.HighestBpReinforceStrategy import (
    HighestBpReinforceStrategy,
)
from src.strategies.reinforce.HighestMpReinforceStrategy import (
    HighestMpReinforceStrategy,
)
from src.strategies.reinforce.CheapestCrabReinforceStrategy import (
    CheapestCrabReinforceStrategy,
)
from src.strategies.reinforce.NoReinforceStrategy import NoReinforceStrategy
from src.strategies.reinforce.ReinforceStrategy import ReinforceStrategy
from src.models.User import User

lootStrategies = {
    "LowestBp": LowestBpLootStrategy,
}

reinforceStrategies = {
    "NoReinforce": NoReinforceStrategy,
    "CheapestCrab": CheapestCrabReinforceStrategy,
    "HighestBp": HighestBpReinforceStrategy,
    "HighestMp": HighestMpReinforceStrategy,
}


def getBestMineToLoot(userAddress: Address, team: Team) -> Game:
    """
    Find best mine to loot for the given team, using the Loot strategy
    provided in the user settings
    """

    # Fetch the strategy name from the user settings
    strategyName = (
        User(userAddress).getTeamConfig(team["team_id"]).get("lootStrategyName")
    )
    if not strategyName:
        raise StrategyNotSet(
            f"Could not find the lootStrategyName setting for team {team['team_id']}"
        )

    # Create the strategy object and use it to get the mine
    strategy: LootStrategy = makeLootStrategy(strategyName, team)
    return strategy.getMine()


def getBestReinforcement(user: User, mine: Game, maxPrice: Tus) -> CrabForLending:
    """
    Find best crab to borrow for the given mine and at the given max price,
    using the Reinforce strategy provided in the user settings
    """

    # Fetch the team involved in the given mine
    (teamConfig, lootingOrMining) = user.getTeamConfigFromMine(mine)
    if not teamConfig:
        raise StrategyException(f"User {user} has no teams in mine {mine['game_id']}")

    # Fetch the strategy name from the user settings
    strategyName = teamConfig.get("reinforceStrategyName")
    if not strategyName:
        raise StrategyNotSet(f"Team {teamConfig['id']} has no reinforce strategy set")

    # Create the strategy object and use it to get the crab to borrow
    strategy: ReinforceStrategy = makeReinforceStrategy(
        strategyName, user, teamConfig, mine, maxPrice
    )

    return strategy.getCrab(lootingOrMining)


def makeLootStrategy(strategyName: str, team: Team) -> LootStrategy:
    """
    Instantiate and return the Loot Strategy with the given name
    and the given parameters
    """
    strategyClass = lootStrategies.get(strategyName)
    if not strategyClass:
        raise StrategyNotFound(f"Cound not find a lootStrategy named {strategyName}")
    if not issubclass(strategyClass, (LootStrategy)):
        raise StrategyException(f"Error fetching loot strategy {strategyName}")
    return strategyClass(crabadaWeb2Client).setParams(team)


def makeReinforceStrategy(
    strategyName: str, user: User, teamConfig: ConfigTeam, mine: Game, maxPrice: Tus
) -> ReinforceStrategy:
    """
    Instantiate and return the Reinforce Strategy with the given name
    and the given parameters
    """
    strategyClass = reinforceStrategies.get(strategyName)
    if not strategyClass:
        raise StrategyNotFound(
            f"Cound not find a reinforceStrategy named {strategyName}"
        )
    if not issubclass(strategyClass, (ReinforceStrategy)):
        raise StrategyException(f"Error fetching reinforce strategy {strategyName}")

    return strategyClass(user, teamConfig, crabadaWeb2Client).setParams(mine, maxPrice)
