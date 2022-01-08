from abc import ABC
from src.libs.CrabadaWeb2Client.CrabadaWeb2Client import CrabadaWeb2Client
from src.libs.CrabadaWeb2Client.types import Game

class Strategy(ABC):
    """Generic strategy"""

    web2Client: CrabadaWeb2Client = None

    def __init__(self, game: Game, web2Client: CrabadaWeb2Client) -> None:
        self.web2Client = CrabadaWeb2Client