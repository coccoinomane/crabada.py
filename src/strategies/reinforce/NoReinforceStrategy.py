from typing import Any, List
from src.libs.CrabadaWeb2Client.types import CrabForLending, Game, TeamStatus
from src.strategies.reinforce.ReinforceStrategy import ReinforceStrategy


class NoReinforceStrategy(ReinforceStrategy):
    """
    Strategy to adopt if you do not wish to reinforce
    at all; useful for auto-lose teams
    """

    def query(self, game: Game) -> List[CrabForLending]:
        """No need to make a query at all"""
        return None

    def handleNoSuitableCrabFound(self, crab: CrabForLending) -> None:
        """No need to raise an exception, as finding no crab is
        the aim of the strategy :-)"""
        pass
