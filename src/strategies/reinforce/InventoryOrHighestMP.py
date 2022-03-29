from typing import Any, List
from src.libs.CrabadaWeb2Client.types import CrabForLending, Game
from src.strategies.reinforce.ReinforceStrategy import ReinforceStrategy
from src.helpers.general import nthOrLastOrNone
from src.helpers.price import weiToTus


class InventoryOrHighestMP(ReinforceStrategy):
    """
    Strategy that chooses the crab with a price lower than maxPrice
    which has the highest mine point value
    """

    def query(self, game: Game) -> dict[str, Any]:
        """ """
        return None

    def getFromInventoryOrTavern(self, game: Game) -> List[CrabForLending]:
        """
        1. Checks inventory first for self/reinforceable crabs.
        2. If no crab is available, uses tavern as usual.
        """
        inventory_crabs = self.web2Client.listCrabsForLendingFromInventory(
            user_address=self.user.address
        )
        if inventory_crabs:
            return inventory_crabs

        params = {
            "limit": 200,  # TODO: make it an argument
            "orderBy": "price",
            "order": "asc",
        }
        return self.web2Client.listCrabsForLending(params)

    def process(self, game: Game, crabs: List[CrabForLending]) -> List[CrabForLending]:

        # query() returns None, so crabs list given here should be empty as well.
        # we can replace it with our custom ultimate-crab-getting-logic
        crabs = self.getFromInventoryOrTavern(game=game)

        affordableCrabs = [c for c in crabs if weiToTus(c["price"]) < self.maxPrice1]
        return sorted(affordableCrabs, key=lambda c: (-c["mine_point"], c["price"]))
