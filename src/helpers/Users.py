from eth_typing import Address
from src.common.config import users

def isRegistered(userAddress: Address) -> bool:
    """Return true if the given user is in the list
    of registered users"""
    return True if [ u for u in users if u['address'] == userAddress ] else False