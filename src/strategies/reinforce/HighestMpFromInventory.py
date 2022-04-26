from typing import List
from src.libs.CrabadaWeb2Client.types import CrabForLending, Game
from src.strategies.reinforce.FirstFromInventory import FirstFromInventory


class HighestMpFromInventory(FirstFromInventory):
    """
    Reinforce with the highest-MP inventory crab available.
    """

    def process(self, game: Game, crabs: List[CrabForLending]) -> List[CrabForLending]:
        crabs = super().process(game, crabs)
        return sorted(crabs, key=lambda c: -c["mine_point"])
