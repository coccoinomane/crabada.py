from typing import Any, List
from src.libs.CrabadaWeb2Client.types import CrabadaClass, Game
from src.strategies.reinforce.ReinforceStrategy import ReinforceStrategy


class CheapestCrab(ReinforceStrategy):
    """
    Strategy that always chooses the cheapest crab for reinforcements
    """

    def query(self, game: Game) -> dict[str, Any]:
        queryParams = {
            "limit": 1,
            "orderBy": "price",
            "order": "asc",
        }

        crabadaClass = self.teamConfig["reinforcementCrabadaClass"]
        if crabadaClass != CrabadaClass.ALL:
            queryParams["class_ids[]"] = crabadaClass.value

        return queryParams
