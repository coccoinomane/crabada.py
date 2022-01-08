from typing import Any, List
from src.libs.CrabadaWeb2Client.types import CrabForLending, Game
from src.strategies.mining import MiningStrategy
from src.helpers.General import firstOrNone, secondOrNone

class CheapestCrabStrategy(MiningStrategy):
    """
    Strategy that always chooses the cheapest crab for reinforcements
    """

    def query1(self, game: Game) -> List[CrabForLending]:
        return {
            "limit": 1,
            "orderBy": 'price',
            "order": 'asc',
        }

    def query2(self, game: Game) -> List[CrabForLending]:
        return self.query1()

    def crab1(self, game: Game, list1: List[CrabForLending]) -> CrabForLending:
        crab = firstOrNone(self.crabsForLending)
        return None if crab.price > self.maxPriceForReinforce1 else crab

    def crab2(self, game: Game, list1: List[CrabForLending]) -> CrabForLending:
        crab = firstOrNone(self.crabsForLending)
        return None if crab.price > self.maxPriceForReinforce2 else crab
