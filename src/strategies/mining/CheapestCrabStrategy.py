from typing import List
from src.libs.CrabadaWeb2Client.types import CrabForLending, Game
from src.strategies.mining.ReinforceStrategy import ReinforceStrategy
from src.helpers.General import firstOrNone, secondOrNone

class CheapestCrabStrategy(ReinforceStrategy):
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
        return self.query1(game)
