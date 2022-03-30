from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Tuple
from src.common.exceptions import StrategyNotApplicable
from src.common.types import ConfigTeam
from src.libs.CrabadaWeb2Client.CrabadaWeb2Client import CrabadaWeb2Client
from src.models.User import User


class Strategy(ABC):
    """
    A generic strategy to be applied to a given game; extend this class
    to make your own strategies.

    A strategy can always use all of the configurations of the user and
    of the team involved; you can access them via self.user and self.teamConfig,
    respectively.
    """

    def __init__(
        self, user: User, teamConfig: ConfigTeam, web2Client: CrabadaWeb2Client
    ) -> None:
        self.user: User = user
        self.teamConfig: ConfigTeam = teamConfig
        self.web2Client: CrabadaWeb2Client = web2Client

    def setParams(self, *args: Any, **kwargs: Any) -> Strategy:
        """
        Set here the parameters of the strategy as class attributes. For example,
        if the strategy needs a maxPrice parameter, the function will need to
        set the maxPrice attribute: self.maxPrice = maxPrice
        """
        return self

    def raiseIfNotApplicable(self) -> None:
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
        return (True, "")
