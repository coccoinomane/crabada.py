from typing import Any, List
from src.helpers.reinforce import convertCrabFromInventory
from src.libs.CrabadaWeb2Client.types.idleGameTypes import CrabForLending, Game
from src.strategies.reinforce.ReinforceStrategy import ReinforceStrategy


class FirstFromInventory(ReinforceStrategy):
    """
    If Inventory Crab is available, reinforce with it.
    """

    def query(self, game: Game) -> dict[str, Any]:
        """
        No need to query the tavern
        """
        return None

    def process(self, game: Game, crabs: List[CrabForLending]) -> List[CrabForLending]:
        """
        query() returns None, so crabs list given here should be empty as
        well; we can replace it with our custom ultimate-crab-getting-logic
        """
        inventoryCrabs = self.web2Client.listCrabsFromInventory(self.user.address)
        return [convertCrabFromInventory(c) for c in inventoryCrabs]
