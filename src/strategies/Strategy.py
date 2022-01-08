from abc import ABC, abstractstaticmethod
from typing import Tuple
from src.common.exceptions import StrategyNotApplicable
from src.libs.CrabadaWeb2Client.CrabadaWeb2Client import CrabadaWeb2Client
from src.libs.CrabadaWeb2Client.types import Game

class Strategy(ABC):
    """
    A generic strategy to be applied to a given game; extend this class
    to make your own strategies.
    
    Your subclass must implement the isApplicable() static method which is
    used to determine if the strategy is applicable to a given game.

    If you also instantiate the strategy with strict=True, an
    error will be raised at instantiation if the strategy is not applicable to
    the game.
    """

    game: Game = None
    web2Client: CrabadaWeb2Client = None

    def __init__(self, game: Game, web2Client: CrabadaWeb2Client, strict: bool = False) -> None:
        self.game = game
        self.web2Client = web2Client
        if strict:
            self.raiseIfNotApplicable()

    def raiseIfNotApplicable(self):
        """
        Raise error if the strategy is not applicable
        """
        isApplicable, msg = self.isApplicable(self.game)
        if not isApplicable:
            raise StrategyNotApplicable(msg or f"The strategy cannot be applied to the current game (game id = {self.game['game_id']})")

    @abstractstaticmethod
    def isApplicable(game: Game) -> Tuple[bool, str]:
        """
        Is the strategy appropriate for the provided game?
        
        Returns a tuple where
        - the first element is either True or False
        - the second is the reason why the strategy is not applicable
        """
        return (True, '')