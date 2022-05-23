from typing import Literal, cast
from eth_typing import Address
from src.helpers.mines import (
    attackIsOver,
    mineHasBeenAttacked,
    mineIsOpen,
    mineIsSettled,
)
from src.libs.CrabadaWeb2Client.types.idleGameTypes import CrabForLending, CrabFromInventory, Game
from web3.types import Wei


def minerCanReinforce(mine: Game) -> bool:
    """
    Return True if, in the given game, the miner (the defense) can
    reinforce at this moment, regardless of whether its the first or the
    second time
    """
    return getMinerReinforcementStatus(mine) != 0


def getMinerReinforcementStatus(mine: Game) -> Literal[0, 1, 2]:
    """
    Determines whether the miner can reinforce and, if this
    is the case, whether the 1st or 2nd reinforcement is
    needed

    Returns:
    - 0 if the miner cannot reinforce
    - 1 if the miner can reinforce for the first time
    - 2 if the miner can reinforce for the second time
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
        mineIsOpen(mine)
        and mineHasBeenAttacked(mine)
        and not attackIsOver(mine)
        and not mineIsSettled(mine)
        and mine["round"] == 0
    )


def minerCanReinforceForTheSecondTime(mine: Game) -> bool:
    """
    Return True if, in the given game, the miner (the defense) can
    reinforce at this moment for the second time
    """
    return (
        mineIsOpen(mine)
        and mineHasBeenAttacked(mine)
        and not attackIsOver(mine)
        and not mineIsSettled(mine)
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
    Determines whether the looter can reinforce and, if this
    is the case, whether the 1st or 2nd reinforcement is
    needed

    Returns:
    - 0 if the looter cannot reinforce
    - 1 if the looter can reinforce for the first time
    - 2 if the looter can reinforce for the second time
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
        mineIsOpen(mine)
        and mineHasBeenAttacked(mine)
        and not attackIsOver(mine)
        and not mineIsSettled(mine)
        and mine["round"] == 1
    )


def looterCanReinforceForTheSecondTime(mine: Game) -> bool:
    """
    Return True if, in the given game, the looter (the attack) can
    reinforce at this moment for the second time
    """
    return (
        mineIsOpen(mine)
        and mineHasBeenAttacked(mine)
        and not attackIsOver(mine)
        and not mineIsSettled(mine)
        and mine["round"] == 3
    )


def convertCrabFromInventory(crab: CrabFromInventory) -> CrabForLending:
    """
    Given a crab from the user's inventory, convert it to a crab
    suitable to be borrowed.

    This is just an interface function needed to use crabs from inventory
    in reinforce strategies, as if they were crabs from the tavern.
    """
    crabForLending = cast(CrabForLending, crab)

    # Price is important, it is required by the contract
    # and we may use it for ordering and stuff...
    crabForLending["price"] = cast(Wei, 0)

    # Others not so much...
    crabForLending["lender"] = cast(Address, "")
    crabForLending["is_being_borrowed"] = 0
    crabForLending["borrower"] = cast(Address, "")
    crabForLending["game_id"] = 0

    return crabForLending
