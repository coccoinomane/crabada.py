from __future__ import annotations
from abc import abstractmethod
from typing import List, Tuple, cast
from src.common.exceptions import CrabBorrowPriceTooHigh, StrategyException
from src.common.types import Tus
from src.helpers.general import firstOrNone
from src.helpers.price import tusToWei, weiToTus
from src.helpers.reinforce import (
    getMinerReinforcementStatus,
    getLooterReinforcementStatus,
    looterCanReinforce,
    minerCanReinforce,
)
from src.strategies.Strategy import Strategy
from src.libs.CrabadaWeb2Client.types import CrabForLending, Game, TeamStatus


class ReinforceStrategy(Strategy):
    """
    Generic strategy to fetch the best possible crab to reinforce
    the given mine.

    Extend this class and override the query(), crab() and,
    optionally, crab2() methods in order to define a complete
    strategy.

    The strategy can be used by calling the crab() method to
    fetch the first reinforcement, and the crab2() method to
    fetch the second one.

    Attributes
    ----------
    game: Game
    maxPrice: Tus
    maxPrice2: Tus
    """

    def setParams(
        self, game: Game, maxPrice: Tus = cast(Tus, 50), maxPrice2: Tus = None
    ) -> Strategy:
        """
        Parameters for a generic reinforce strategy

        :param Game game: The game to apply the strategy to
        :param Tus maxPrice: Max price to spend for the first reinforcement, in Tus
        :param Tus maxPrice2: Max price to spend for the second reinforcement, in Tus;
        leave it blank to use the same value as maxPrice1
        """
        self.game: Game = game
        self.maxPrice1: Tus = maxPrice
        self.maxPrice2: Tus = maxPrice2 if maxPrice2 else self.maxPrice1
        return self

    def isApplicable(self) -> Tuple[bool, str]:
        """
        The strategy can be applied only if the mine can
        be reinforced
        """
        isApplicable = minerCanReinforce(self.game) or looterCanReinforce(self.game)
        return (
            isApplicable,
            ""
            if isApplicable
            else f"Game cannot be reinforced (mine_id = {self.game['game_id']}, round = {self.game['round']}, winner_team_id = {self.game['winner_team_id']})",
        )

    @abstractmethod
    def query(self, game: Game) -> List[CrabForLending]:
        """
        Query to get the list of the available crabs for lending,
        from which we will choose the reinforcement.
        """
        return []

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

    def getCrab(self, lootingOrMining: TeamStatus) -> CrabForLending:
        """
        Fetch and return a reinforcement crab, using the strategy;
        if no crab can be found, return None.

        Contrary to getCrab1 and getCrab2, this function automatically decides
        which reinforcement (first vs second) is needed based on the game's
        status. This is why it needs to know whether your team is mining or
        looting.
        """

        if lootingOrMining == "LOOTING":
            status = getLooterReinforcementStatus(self.game)
        elif lootingOrMining == "MINING":
            status = getMinerReinforcementStatus(self.game)
        else:
            raise StrategyException(
                f"Team is neither LOOTING nor MINING, [value passed={lootingOrMining}]"
            )

        if status == 0:  # mine cannot be reinforced
            return None
        elif status == 1:  # first reinforcement
            return self._getCrab1()
        elif status == 2:  # second reinforcement
            return self._getCrab2()

    def raiseIfPriceTooHigh(self, crab: CrabForLending, maxPrice: Tus) -> None:
        """
        Raise an exception if the price of the given crab is higher
        than the given max price; the latter should be give in TUS,
        not wei
        """
        if crab["price"] > tusToWei(maxPrice):
            raise CrabBorrowPriceTooHigh(
                f"Crab's price {weiToTus(crab['price'])} higher than max {maxPrice}"
            )

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
