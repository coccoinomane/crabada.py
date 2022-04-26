from typing import Any
from src.libs.CrabadaWeb2Client.types import Game
from src.strategies.reinforce.HighestBp import HighestBp


class HighestBpHighCost(HighestBp):
    """
    Fetch the highest-BP crabs in the tavern, then pick the
    cheapest one that costs less than maxPrice.

    If the reinforcementToPick mechanism is active, it avoids
    choosing highly requested crabs that could result in failed
    txs.
    """

    def query(self, game: Game) -> dict[str, Any]:
        return {
            "limit": 100,
            "orderBy": "battle_point",
            "order": "desc",
        }
