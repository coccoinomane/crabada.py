from typing import Any, List
from src.libs.CrabadaWeb2Client.types import CrabForLending, Game
from src.strategies.reinforce.ReinforceStrategy import ReinforceStrategy
from src.helpers.general import firstOrNone
from src.helpers.price import weiToTus


class HighestBpReinforceStrategy(ReinforceStrategy):
    """
    Strategy that chooses the crab with a price lower than maxPrice
    which has the highest battle point value
    """

    def query(self, game: Game) -> dict[str, Any]:
        return {
            "limit": 200,  # TODO: make it an argument
            "orderBy": "price",
            "order": "asc",
        }

    def process(self, game: Game, list: List[CrabForLending]) -> List[CrabForLending]:
        affordableCrabs = [c for c in list if weiToTus(c["price"]) < self.maxPrice1]
        if len(affordableCrabs) == 0:
            return None
        return sorted(affordableCrabs, key=lambda c: (-c["battle_point"], c["price"]))

    def pick(self, game: Game, list: List[CrabForLending]) -> CrabForLending:
        return firstOrNone(list)
