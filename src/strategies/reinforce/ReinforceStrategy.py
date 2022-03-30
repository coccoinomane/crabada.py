from __future__ import annotations
from abc import abstractmethod
from typing import List, Tuple, cast
from src.common.exceptions import (
    ReinforcementTooExpensive,
    NoSuitableReinforcementFound,
    StrategyException,
)
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

    To define a complete strategy, extend this class and override
    the query(), process() and pick() methods.

    If you need a different criterion for the 2nd reinforcement, you
    can optionally, override any of query2(), process2() or pick2().

    The preferred way to use the strategy is to call getCrab(), which
    returns the needed reinforcement crab based on the status of the
    mine, or None if the mining/looting team cannot be reinforced.

    If needed, you can also call getCrab1() and getCrab2() which will
    always return a crab regardless of the status of the mine.

    Attributes
    ----------
    game: Game
    maxPrice: Tus
    maxPrice2: Tus
    """

    def setParams(self, game: Game, maxPrice: Tus, maxPrice2: Tus = None) -> Strategy:
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
            else f"Game cannot be reinforced [mine_id = {self.game['game_id']}, round = {self.game['round']}, winner_team_id = {self.game['winner_team_id']}]",
        )

    @abstractmethod
    def query(self, game: Game) -> List[CrabForLending]:
        """
        Query for the Crabada endpoint that will fetch the available
        crabs for lending, from which we will pick our reinforcement.
        """
        return []

    def process(self, game: Game, crabs: List[CrabForLending]) -> List[CrabForLending]:
        """
        Process the list of available reinforcements fetched with
        the query() method.

        A typical processing is to sort the list by price or stats,
        or filter it according to some criterion.

        By default, return the list unchanged.
        """
        return crabs

    def pick(self, game: Game, crabs: List[CrabForLending]) -> CrabForLending:
        """
        Pick the reinforcement crab from the processed list of available
        crabs.

        By default, pick the first crab in the list.
        """
        return firstOrNone(crabs)

    def query2(self, game: Game) -> List[CrabForLending]:
        """
        Optionally specify a separate query for the second reinforcement
        """
        return self.query(game)

    def process2(self, game: Game, list: List[CrabForLending]) -> List[CrabForLending]:
        """
        Optionally specify a separate process for the second reinforcement
        """
        return self.process(game, list)

    def pick2(self, game: Game, list: List[CrabForLending]) -> CrabForLending:
        """
        Optionally specify a separate selection criterion for the
        second reinforcement
        """
        return self.pick(game, list)

    def getCrab(self, lootingOrMining: TeamStatus) -> CrabForLending:
        """
        Fetch and return a reinforcement crab, using the strategy;
        if no crab can be found, return None.

        Contrary to getCrab1() and getCrab2(), this method automatically decides
        which reinforcement (first vs second) is needed based on the game's
        status, and it returns None if the game cannot be reinforced.
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
            return self.getCrab1()
        elif status == 2:  # second reinforcement
            return self.getCrab2()

    def handleNoSuitableCrabFound(self, crab: CrabForLending) -> None:
        """
        By default, raise an exception if the strategy is unable to find
        a suitable crab
        """
        raise NoSuitableReinforcementFound(
            f"Could not find a suitable reinforcement [strategy={self.__class__.__name__}]"
        )

    def handlePriceTooHigh(self, crab: CrabForLending, maxPrice: Tus) -> None:
        """
        By default, raise an exception if the price of the given crab is
        higher than the strategy's max price
        """
        raise ReinforcementTooExpensive(
            f"Crab's price is higher than max {maxPrice} TUS [price={weiToTus(crab['price'])}, strategy={self.__class__.__name__}]"
        )

    def getCrab1(self) -> CrabForLending:
        """
        Fetch and return a reinforcement crab using the strategy set in
        query(), process() and pick(). If no crab can be found, return None.
        """
        query = self.query(self.game)

        # Get the list of borrowable reinforcements from Crabada
        crabs = self.web2Client.listCrabsForLending(query) if query is not None else []

        # Process the list of crabs
        processedCrabs = self.process(self.game, crabs)

        # Select the crab based on the strategy
        crab = self.pick(self.game, processedCrabs)

        # Handle special cases
        if not crab:
            self.handleNoSuitableCrabFound(crab)
        elif crab["price"] > tusToWei(self.maxPrice1):
            self.handlePriceTooHigh(crab, self.maxPrice1)

        return crab

    def getCrab2(self) -> CrabForLending:
        """
        Fetch and return a reinforcement crab using the strategy set in
        query2(), process2() and pick2(). If no crab can be found, return None.
        """
        query = self.query2(self.game)

        # Get the list of borrowable reinforcements from Crabada
        crabs = self.web2Client.listCrabsForLending(query) if query is not None else []

        # Process the list of crabs
        processedCrabs = self.process2(self.game, crabs)

        # Select the crab based on the strategy
        crab = self.pick2(self.game, processedCrabs)

        # Handle special cases
        if not crab:
            self.handleNoSuitableCrabFound(crab)
        elif crab["price"] > tusToWei(self.maxPrice2):
            self.handlePriceTooHigh(crab, self.maxPrice2)

        return crab
