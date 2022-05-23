from typing import Any, List
from src.libs.CrabadaWeb2Client.types.idleGameTypes import CrabForLending, Game, TeamStatus
from src.strategies.reinforce.ReinforceStrategy import ReinforceStrategy


class NoReinforceStrategy(ReinforceStrategy):
    """
    Strategy to adopt if you do not wish to reinforce
    at all; useful for auto-lose teams
    """

    def query(self, game: Game) -> dict[str, Any]:
        """No need to make a query at all"""
        return None

    def handleNoSuitableCrabFound(self) -> None:
        """No need to alert the user, because finding no crab is
        the aim of the strategy :-)"""
        pass

    def mayReturnNone(self) -> bool:
        """Do not worry if this strategy returns no result"""
        return True
