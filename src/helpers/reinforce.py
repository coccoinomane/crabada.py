from typing import Literal
from eth_typing.evm import Address
from web3.types import Wei
from src.common.exceptions import MissingConfig
from src.helpers.mines import mineHasBeenAttacked, mineIsOpen, mineReadyToBeSettled
from src.models.User import User
from src.libs.CrabadaWeb2Client.types import Game


def minerCanReinforce(mine: Game) -> bool:
    """
    Return True if, in the given game, the miner (the defense) can
    reinforce at this moment, regardless of whether its the first or the
    second time
    """
    return getMinerReinforcementStatus(mine) != 0


def getMinerReinforcementStatus(mine: Game) -> Literal[0, 1, 2]:
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
    """
    Return True if, in the given game, the miner (the defense) can
    reinforce at this moment for the first time
    """
    return (
        not mineReadyToBeSettled(mine)
        and mineHasBeenAttacked(mine)
        and mineIsOpen(mine)
        and mine["round"] == 0
    )


def minerCanReinforceForTheSecondTime(mine: Game) -> bool:
    """
    Return True if, in the given game, the miner (the defense) can
    reinforce at this moment for the second time
    """
    return (
        not mineReadyToBeSettled(mine)
        and mineHasBeenAttacked(mine)
        and mineIsOpen(mine)
        and mine["round"] == 2
    )


def looterCanReinforce(mine: Game) -> bool:
    """
    Return True if, in the given game, the looter (the attack) can
    reinforce at this moment, regardless of whether its the first or the
    second time
    """
    return getLooterReinforcementStatus(mine) != 0


def getLooterReinforcementStatus(mine: Game) -> Literal[0, 1, 2]:
    """
    Determines whether the game can be reinforced and
    at which reinforcement stage we are.

    Returns:
    - 0 if the mine cannot be reinforced
    - 1 if the mine can be reinforced the first time
    - 2 if the mine can be reinforced the second time
    """
    if looterCanReinforceForTheFirstTime(mine):
        return 1
    elif looterCanReinforceForTheSecondTime(mine):
        return 2
    else:
        return 0


def looterCanReinforceForTheFirstTime(mine: Game) -> bool:
    """
    Return True if, in the given game, the looter (the attack) can
    reinforce at this moment for the first time
    """
    return (
        not mineReadyToBeSettled(mine)
        and mineHasBeenAttacked(mine)
        and mineIsOpen(mine)
        and mine["round"] == 1
    )


def looterCanReinforceForTheSecondTime(mine: Game) -> bool:
    """
    Return True if, in the given game, the looter (the attack) can
    reinforce at this moment for the second time
    """
    return (
        not mineReadyToBeSettled(mine)
        and mineHasBeenAttacked(mine)
        and mineIsOpen(mine)
        and mine["round"] == 3
    )


def reinforcementIsTooExpensive(price: Wei, userAddress: Address) -> bool:
    """
    Return True if the given price is too much for lending a
    reinforcement crab.

    The price must be given as it is returned by the listCrabsForLending
    endpoint, that is, in Wei, that is, in units of 1e-18 TUS."""
    maxPrice = User(userAddress).config.get("reinforcementMaxPriceInTusWei")
    return price > maxPrice
