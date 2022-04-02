from typing import Any, List
from src.libs.CrabadaWeb2Client.types import Game
from src.strategies.reinforce.ReinforceStrategy import ReinforceStrategy


class CheapestCrab(ReinforceStrategy):
    """
    Strategy that always chooses the cheapest crab for reinforcements
    """

    def query(self, game: Game) -> dict[str, Any]:
        return {
            "limit": 1,
            "orderBy": "price",
            "order": "asc",
        }
