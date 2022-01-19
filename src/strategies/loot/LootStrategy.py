from abc import abstractmethod
from typing import List, Tuple
from src.helpers.general import firstOrNone
from src.helpers.teams import teamCanLoot
from src.strategies.Strategy import Strategy
from src.libs.CrabadaWeb2Client.types import Game, Team

class LootStrategy(Strategy):
    """
    Generic looting strategy, consisting in finding the perfect
    mine to loot, given a looter team.
    """

    team: Team = None # team to send looting
    minesToFetch: int = None # number of mines to consider, the lowest the fastest
    lootableMines: List[Game] = []

    def setParams(self, team: Team, minesToFetch: int = 5) -> Strategy:
        self.team = team
        self.minesToFetch = minesToFetch
        return self

    def isApplicable(self) -> Tuple[bool, str]:
        """
        The strategy can be applied only if the team is busy
        """
        isApplicable = teamCanLoot(self.team)
        return (
            isApplicable,
            '' if isApplicable else f"Team cannot loot {self.team['team_id']} (status = {self.team['status']})"
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
        self.lootableMines = self.web2Client.listMines(self.query(self.team))
        return self.mine(self.team, self.lootableMines)
