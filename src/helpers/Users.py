from eth_typing import Address
from src.common.config import users
from src.common.types import ConfigUser
from src.helpers.General import firstOrNone

def getUserConfig(userAddress: Address) -> ConfigUser:
    """Return a user configuration given its address;
    returns None if no user with that address is found"""
    return firstOrNone([ u for u in users if u['address'] == userAddress ])

def isRegistered(userAddress: Address) -> bool:
    """Return true if the given user is in the list
    of registered users"""
    return True if getUserConfig(userAddress) else False