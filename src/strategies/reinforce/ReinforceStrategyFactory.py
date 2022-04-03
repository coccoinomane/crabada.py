"""
Use the "make" function defined in this class to dinamically
instantiate strategies.

Also provides utility function to easily return products of
strategies (mine, crab, etc) without having to type boilerplate.
"""

from src.common.logger import logger
from src.common.exceptions import (
    NoSuitableReinforcementFound,
    StrategyException,
    StrategyNotFound,
)
from src.common.clients import crabadaWeb2Client
from src.common.types import ConfigTeam, Tus
from src.libs.CrabadaWeb2Client.types import CrabForLending, Game, Team, TeamStatus
from src.strategies.reinforce.HighestBp import HighestBp
from src.strategies.reinforce.HighestBpFromInventory import HighestBpFromInventory
from src.strategies.reinforce.HighestMp import HighestMp
from src.strategies.reinforce.HighestBpHighCost import HighestBpHighCost
from src.strategies.reinforce.FirstFromInventory import FirstFromInventory
from src.strategies.reinforce.HighestMpFromInventory import HighestMpFromInventory
from src.strategies.reinforce.HighestMpHighCost import HighestMpHighCost
from src.strategies.reinforce.CheapestCrab import CheapestCrab
from src.strategies.reinforce.NoReinforceStrategy import NoReinforceStrategy
from src.strategies.reinforce.ReinforceStrategy import ReinforceStrategy
from src.models.User import User

reinforceStrategies = {
    "NoReinforce": NoReinforceStrategy,
    "CheapestCrab": CheapestCrab,
    "HighestBp": HighestBp,
    "HighestMp": HighestMp,
    "HighestBpHighCost": HighestBpHighCost,
    "HighestMpHighCost": HighestMpHighCost,
    "FirstFromInventory": FirstFromInventory,
    "HighestBpFromInventory": HighestBpFromInventory,
    "HighestMpFromInventory": HighestMpFromInventory,
}


def getBestReinforcement(
    user: User,
    mine: Game,
    maxPrice: Tus,
    teamConfig: ConfigTeam = None,
    lootingOrMining: TeamStatus = None,
) -> CrabForLending:
    """
    Find best crab to borrow for the given mine and at the given max price,
    using the first suitable Reinforce strategy provided in the user settings
    """

    # Fetch the team involved in the given mine
    if not teamConfig or not lootingOrMining:
        (teamConfig, lootingOrMining) = user.getTeamConfigFromMine(mine)
        if not teamConfig:
            raise StrategyException(
                f"User {user} has no teams in mine {mine['game_id']}"
            )

    crab: CrabForLending = None

    # Return the crab to borrow using the first suitable strategy
    for strategyName in teamConfig["reinforceStrategies"]:
        strategy: ReinforceStrategy = makeReinforceStrategy(
            strategyName, user, teamConfig, mine, maxPrice
        )
        crab = strategy.getCrab(lootingOrMining)
        if crab or strategy.mayReturnNone():
            return crab

    raise NoSuitableReinforcementFound(
        f"No suitable reinforcement found [mine={mine['game_id']}, team={teamConfig['id']}]"
    )


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
