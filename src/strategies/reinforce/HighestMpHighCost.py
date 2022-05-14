from typing import Any
from src.libs.CrabadaWeb2Client.types import CrabadaClass, Game
from src.strategies.reinforce.HighestMp import HighestMp


class HighestMpHighCost(HighestMp):
    """
    Fetch the highest-MP crabs in the tavern, then pick the
    cheapest one that costs less than maxPrice.

    If the reinforcementToPick mechanism is active, it avoids
    choosing highly requested crabs that could result in failed
    txs.
    """

    def query(self, game: Game) -> dict[str, Any]:
        queryParams = {
            "limit": 100,
            "orderBy": "time_point",
            "order": "desc",
        }

        if self.teamConfig["reinforcementCrabadaClass"] != CrabadaClass.ALL:
            queryParams["class_ids[]"] = self.teamConfig["reinforcementCrabadaClass"]

        return queryParams
