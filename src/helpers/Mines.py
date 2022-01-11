"""
Helper functions to handle Crabada mines / gamess
"""

from typing import List
from src.helpers.Dates import getPrettySeconds
from time import time
from src.common.clients import crabadaWeb2Client
from src.helpers.General import firstOrNone
from src.libs.CrabadaWeb2Client.types import Game

def mineHasBeenAttacked(mine: Game) -> bool:
    """
    Return True if, in the given game, the miner (the defense) has
    been attacked
    """
    return mine['attack_team_id'] is not None

def mineIsOpen(mine: Game) -> bool:
    """
    Return True if the given game is open
    """
    return mine['status'] == 'open'

def mineIsSettled(mine: Game) -> bool:
    """
    Return True if the given game is settled
    """
    return mine['winner_team_id'] is not None

def mineIsFinished(game: Game) -> bool:
    """
    Return true if the given game is past its end_time
    """
    return getRemainingTime(game) <= 0

def mineIsClosed(game: Game) -> bool:
    """
    Return true if the given game is closed (meaning the
    game has been settled and the reward has been claimed)
    """
    return game['status'] == 'close'

def getRemainingTime(game: Game) -> int:
    """
    Seconds to the end of the given game
    """
    return int(game['end_time'] - time())

def getRemainingTimeFormatted(game: Game) -> str:
    """
    Hours, minutes and seconds to the end of the given game
    """
    return getPrettySeconds(getRemainingTime(game))

def getNextMineToFinish(games: List[Game]) -> Game:
    """Given a list of games, return the mine that is open and
    next to finish; returns None if there are no unfinished games
    (finished=past the 4th our, regardless of whether the reward
    has been claimed)
    
    If a game is already finished, it won't be considered"""
    unfinishedGames = [ g for g in games if not mineIsFinished(g) ]
    return firstOrNone(sorted(unfinishedGames, key=lambda g: g['end_time']))