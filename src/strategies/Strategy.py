from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Tuple
from src.common.exceptions import StrategyNotApplicable
from src.libs.CrabadaWeb2Client.CrabadaWeb2Client import CrabadaWeb2Client
from src.libs.CrabadaWeb2Client.types import Game

class Strategy(ABC):
    """
    A generic strategy to be applied to a given game; extend this class
    to make your own strategies.
    """

    web2Client: CrabadaWeb2Client = None

    def __init__(self, web2Client: CrabadaWeb2Client) -> None:
        self.web2Client = web2Client

    def setParams(*args, **kwargs) -> Strategy:
        """
        Set here the parameters of the strategy as class attributes. For example,
        if the strategy needs a maxPrice parameter, the will just to set the
        maxPrice attribute: self.maxPrice = maxPrice
        """
        pass

    def raiseIfNotApplicable(self):
        """
        Raise error if the strategy is not applicable
        """
        isApplicable, msg = self.isApplicable()
        if not isApplicable:
            raise StrategyNotApplicable(msg or f"The strategy cannot be applied")

    @abstractmethod
    def isApplicable(self) -> Tuple[bool, str]:
        """
        Is the strategy appropriate for the provided game?
        
        Returns a tuple where
        - the first element is either True or False
        - the second is the reason why the strategy is not applicable
        """
        return (True, '')