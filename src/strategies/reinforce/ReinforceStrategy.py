from __future__ import annotations
from abc import abstractmethod
from typing import Any, List, Tuple
from src.common.exceptions import CrabBorrowPriceTooHigh
from src.common.types import Tus
from src.helpers.General import firstOrNone
from src.helpers.Price import tusToWei, weiToTus
from src.helpers.Reinforce import getReinforcementStatus, minerCanReinforce
from src.strategies.Strategy import Strategy
from src.libs.CrabadaWeb2Client.types import CrabForLending, Game

class ReinforceStrategy(Strategy):
    """
    Generic mining strategy, assuming the game has already
    started
    """

    game: Game = None # game to apply the strategy to
    maxPrice1: Tus = None # max price to spend for the first reinforcement, in Tus
    maxPrice2: Tus = None # max price to spend for the second reinforcement, in Tus

    def setParams(self, game: Game, maxPrice: Tus = 50, maxPrice2: Tus = None) -> Strategy:
        self.game = game
        self.maxPrice1 = maxPrice
        if not maxPrice2:
            self.maxPrice2 = self.maxPrice1
        else:
            self.maxPrice2 = maxPrice2
        return self

    def isApplicable(self) -> Tuple[bool, str]:
        """
        The strategy can be applied only if the mine can
        be reinforced
        """
        isApplicable = minerCanReinforce(self.game)
        return (
            isApplicable,
            '' if isApplicable else f"Miner cannot reinforce mine {self.game['self.game_id']} (round = {self.game['round']}, winner_team_id = {self.game['winner_team_id']})",
        )

    @abstractmethod
    def query(self, game: Game) -> List[CrabForLending]:
        """
        Query to get the list of the available crabs for lending,
        from which we will choose the reinforcement.
        """
        pass

    def query2(self, game: Game) -> List[CrabForLending]:
        """
        Optionally specify a separate query for the second reinforcement
        """
        return self.query(game)

    def crab(self, game: Game, list: List[CrabForLending]) -> CrabForLending:
        """
        Strategy to pick the first reinforcement crab from the list of
        available crabs; by default simply pick the first of the list.
        """
        return firstOrNone(list)

    def crab2(self, game: Game, list: List[CrabForLending]) -> CrabForLending:
        """
        Optionally specify a separate strategy for the second crab
        """
        return self.crab(game, list)

    def getCrab(self) -> CrabForLending:
        """
        Fetch and return a reinforcement crab, using the strategy.
        If no crab can be found, return None.
        """
        status = getReinforcementStatus(self.game)
        if status == 0:
            return None
        elif status == 1:
            return self._getCrab1()
        elif status == 2:
            return self._getCrab2()

    def raiseIfPriceTooHigh(self, crab: CrabForLending, maxPrice: Tus):
        """
        Raise an exception if the price of the given crab is higher
        than the given max price; the latter should be give in TUS,
        not wei
        """
        if crab['price'] > tusToWei(maxPrice):
            raise CrabBorrowPriceTooHigh(f"Crab's price {weiToTus(crab['price'])} higher than max {maxPrice}")

    def _getCrab1(self) -> CrabForLending:
        """
        Fetch and return a reinforcement crab using the strategy set in
        query1() and crab1(). If no crab can be found, return None.
        """
        crabsForLending = self.web2Client.listCrabsForLending(self.query(self.game))
        crab = self.crab(self.game, crabsForLending)
        self.raiseIfPriceTooHigh(crab, self.maxPrice1)
        return crab

    def _getCrab2(self) -> CrabForLending:
        """
        Fetch and return a reinforcement crab using the strategy set in
        query2() and crab2(). If no crab can be found, return None.
        """
        crabsForLending = self.web2Client.listCrabsForLending(self.query2(self.game))
        crab = self.crab2(self.game, crabsForLending)
        self.raiseIfPriceTooHigh(crab, self.maxPrice2)
        return crab
