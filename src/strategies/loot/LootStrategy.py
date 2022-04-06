from abc import abstractmethod
from typing import List, Tuple
from src.helpers.general import firstOrNone
from src.strategies.Strategy import Strategy
from src.libs.CrabadaWeb2Client.types import Game, Team


class LootStrategy(Strategy):
    """
    Generic looting strategy, consisting in finding the perfect
    mine to loot, given a looter team.

    TODO: Implement factional advantage.
    """

    def setParams(self, team: Team, minesToFetch: int = 5) -> Strategy:
        """
        Parameters for a generic looting strategy

        :param Team team: The team to send looting
        :param int minesToFetch: number of mines to consider for looting,
        the lowest the fastest
        """
        self.team: Team = team
        self.minesToFetch: int = minesToFetch
        return self

    def isApplicable(self) -> Tuple[bool, str]:
        """
        The strategy can be applied only if the team is busy
        """
        isApplicable = self.team["status"] == "AVAILABLE"
        return (
            isApplicable,
            ""
            if isApplicable
            else f"Team '{self.team['team_id']}' cannot loot (status = {self.team['status']})",
        )

    @abstractmethod
    def query(self, team: Team) -> List[Game]:
        """
        Query to get the list of the available mines to loot
        """
        pass

    def mine(self, team: Team, list: List[Game]) -> Game:
        """
        Strategy to pick the mine to loot the list of available
        mines; by default simply pick the first of the list.
        """
        return firstOrNone(list)

    def getMine(self) -> Game:
        """
        Fetch and return a mine to loot, using the strategy.
        If no mine can be found, return None.
        """
        lootableMines = self.web2Client.listMines(self.query(self.team))
        return self.mine(self.team, lootableMines)
