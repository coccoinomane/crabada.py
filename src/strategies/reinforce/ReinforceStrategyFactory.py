"""
Use the "make" functions defined in this class to dinamically
instantiate strategies.

Also provides utility function to easily return products of
strategies (mine, crab, etc) without having to type boilerplate.
"""

from src.common.exceptions import StrategyException, StrategyNotFound, StrategyNotSet
from src.common.clients import crabadaWeb2Client
from src.common.types import ConfigTeam, Tus
from src.libs.CrabadaWeb2Client.types import CrabForLending, Game, Team
from src.strategies.reinforce.HighestBp import HighestBp
from src.strategies.reinforce.HighestMp import HighestMp
from src.strategies.reinforce.CheapestCrab import CheapestCrab
from src.strategies.reinforce.NoReinforceStrategy import NoReinforceStrategy
from src.strategies.reinforce.ReinforceStrategy import ReinforceStrategy
from src.models.User import User

reinforceStrategies = {
    "NoReinforce": NoReinforceStrategy,
    "CheapestCrab": CheapestCrab,
    "HighestBp": HighestBp,
    "HighestMp": HighestMp,
}


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
