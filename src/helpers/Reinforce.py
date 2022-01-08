from typing import Literal
from eth_typing.evm import Address
from web3.types import Wei
from src.common.exceptions import MissingConfig

from src.helpers.Users import getUserConfig
from src.libs.CrabadaWeb2Client.types import Game

def isTooExpensiveForUser(price: Wei, userAddress: Address) -> bool:
    """Return True if the given price is too much for lending a
    reinforcement crab. The price must be given as it is returned
    by the listCrabsForLending endpoint, that is, in units of 1e-18
    TUS."""
    maxPrice = getUserConfig(userAddress).get('maxPriceToReinforceInTusWei')
    # TODO: move to config validation
    if not maxPrice or maxPrice <= 0:
        raise MissingConfig("User has no or invalid MAX_PRICE_TO_REINFORCE (must be a value greater than zero)")
    return price > maxPrice

def minerCanReinforce(mine: Game) -> bool:
    """Return True if, in the given game, the miner (the defense) can
    reinforce at this moment, regardless of whether its the first or the
    second time"""
    return getReinforcementStatus(mine) != 0

def getReinforcementStatus(mine: Game) -> Literal[0,1,2]:
    """
    Determines whether the game can be reinforced and
    at which reinforcement stage we are.

    Returns:
    - 0 if the mine cannot be reinforced
    - 1 if the mine can be reinforced the first time
    - 2 if the mine can be reinforced the second time
    """
    if minerCanReinforceForTheFirstTime(mine):
        return 1
    elif minerCanReinforceForTheSecondTime(mine):
        return 2
    else:
        return 0

def minerCanReinforceForTheFirstTime(mine: Game) -> bool:
    """Return True if, in the given game, the miner (the defense) can
    reinforce at this moment for the first time"""
    return (
        mine['winner_team_id'] is None
        and mine['attack_point'] > 0
        and mine['status'] == 'open'
        and mine['round'] == 0
    )

def minerCanReinforceForTheSecondTime(mine: Game) -> bool:
    """Return True if, in the given game, the miner (the defense) can
    reinforce at this moment for the second time"""
    return (
        mine['winner_team_id'] is None
        and mine['attack_point'] > 0
        and mine['status'] == 'open'
        and mine['round'] == 2
    )