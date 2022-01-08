from abc import abstractmethod
from typing import List
from src.strategies.Strategy import Strategy
from src.libs.CrabadaWeb2Client.types import CrabForLending, Game
from src.common.clients import crabadaWeb2Client, crabadaWeb3Client

class MiningStrategy(Strategy):
    """
    Generic mining strategy, assuming the game has already
    started
    """

    game: Game = None # game to apply the strategy to
    maxPrice1: int = 60 # max price to spend for crab1, in Tus
    maxPrice2: int = 60 # max price to spend for crab2, in Tus
    list1: List[CrabForLending] = []
    list2: List[CrabForLending] = []

    @abstractmethod
    def query1(self, game: Game) -> List[CrabForLending]:
        """Query to get the available crabs for lending, for the
        first reinforcement"""
        pass

    @abstractmethod
    def query2(self, game: Game) -> List[CrabForLending]:
        """Query to get the available crabs for lending, for the
        second reinforcement"""
        pass

    @abstractmethod
    def crab1(self, game: Game, list1: List[CrabForLending]) -> CrabForLending:
        """Strategy to get the first reinforcement crab; the game will always
        be at round 0"""
        pass

    @abstractmethod
    def crab2(self, game: Game, list2: List[CrabForLending]) -> CrabForLending:
        """Strategy to get the first reinforcement crab; the game will always
        be at round 2"""
        pass
    
    def getCrab1(self) -> CrabForLending:
        """Fetch and return a reinforcement crab using query1 and crab1;
        if the game is not at the correct stage, return False. If no crab
        can be found, return None."""
        self.list1 = self.web2Client.listCrabsForLending(self.query1(self.game))
        return self.crab1(self.game, self.list1)

    def getCrab2(self) -> CrabForLending:
        """Fetch and return a reinforcement crab using query2 and crab2;
        if the game is not at the correct stage, return False. If no crab
        can be found, return None."""
        self.list2 = self.web2Client.listCrabsForLending(self.query2(self.game))
        return self.crab2(self.game, self.list2)