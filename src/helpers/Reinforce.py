from eth_typing.evm import Address
from web3.types import Wei
from src.common.exceptions import MissingConfig

from src.helpers.Users import getUserConfig

def isTooExpensiveForUser(price: Wei, userAddress: Address) -> bool:
    """Return True if the given price is too much for lending a
    reinforcement crab. The price must be given as it is returned
    by the listCrabsForLending endpoint, that is, in units of 1e-18
    TUS."""
    maxPrice = getUserConfig(userAddress).get('maxPriceToReinforceInTusWei')
    if not maxPrice or maxPrice <= 0:
        raise MissingConfig("User has no or invalid MAX_PRICE_TO_REINFORCE (must be a value greater than zero)")
    return price > maxPrice
    