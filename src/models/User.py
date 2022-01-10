from __future__ import annotations
from eth_typing import Address
from src.common.config import users
from src.common.exceptions import UserException
from src.common.types import ConfigTeam, ConfigUser
from src.helpers.General import findInList, firstOrNone
from src.models.Model import Model

class User(Model):
    """
    A user with his/her configuration, uniquely identified by
    its wallet address
    """

    config: ConfigUser = None

    def __init__(self, userAddress: Address):
        self.config = User.getUserConfig(userAddress)
        if not self.config:
            raise UserException("User address not registered: {userAddress}")

    def getTeamConfig(self, teamId: int) -> ConfigTeam:
        """
        Return the configuration of the user's team with given the team ID
        """
        return findInList(self.config['teams'], 'id', teamId)

    @staticmethod
    def isRegistered(userAddress: Address) -> bool:
        """Return true if the given user is in the list
        of registered users"""
        return True if User.getUserConfig(userAddress) else False

    @staticmethod
    def getUserConfig(userAddress: Address) -> ConfigUser:
        """Return a user configuration given its address;
        returns None if no user with that address is found"""
        return firstOrNone([ u for u in users if u['address'] == userAddress ])

    @staticmethod
    def create(userAddress: Address) -> User:
        """
        User factory
        """
        return User(userAddress)