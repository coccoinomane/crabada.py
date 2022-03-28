"""
Helper functions to handle Crabada mines / games
"""

from typing import List
from src.helpers.dates import getPrettySeconds
from time import time
from src.common.clients import crabadaWeb2Client
from src.helpers.general import firstOrNone
from src.libs.CrabadaWeb2Client.types import Game
from src.models.User import User


def mineHasBeenAttacked(mine: Game) -> bool:
    """
    Return True if, in the given game, the miner (the defense) has
    been attacked
    """
    return mine["attack_team_id"] is not None


def mineIsOpen(mine: Game) -> bool:
    """
    Return True if the given game is open
    """
    return mine["status"] == "open"


def mineReadyToBeSettled(mine: Game) -> bool:
    """
    Return True if the given game is ready to be settled
    """
    # TODO: Update to account for the situation where the looting team has less
    # BP than the mining team since the beginning, in which case you get a weird
    # situation where the mine['winner_team_id'] is None. Maybe use process?
    # Example:
    # [{'game_id': 787426, 'start_time': 1643482620, 'end_time': 1643497020, 'cra_reward': 3750000000000000000, 'tus_reward': 303750000000000000000, 'miner_cra_reward': 3750000000000000000, 'miner_tus_reward': 303750000000000000000, 'looter_cra_reward': 300000000000000000, 'looter_tus_reward': 24300000000000000000, 'estimate_looter_win_cra': 2737500000000000000, 'estimate_looter_win_tus': 221737500000000000000, 'estimate_looter_lose_cra': 300000000000000000, 'estimate_looter_lose_tus': 24300000000000000000, 'estimate_miner_lose_cra': 1312500000000000000, 'estimate_miner_lose_tus': 106312500000000000000, 'estimate_miner_win_cra': 3750000000000000000, 'estimate_miner_win_tus': 303750000000000000000, 'round': 0, 'team_id': 6264, 'owner': '0x7ee27ef2ba8535f83798c930255d7bb5d04aeae8', 'defense_point': 711, 'defense_mine_point': 198, 'attack_team_id': 4476, 'attack_team_owner': '0x5818a5f1ff6df3b7f5dad8ac66e100cce9e33e8e', 'attack_point': 647, 'winner_team_id': None, 'status': 'open', 'process': [{'action': 'create-game', 'transaction_time': 1643482620}, {'action': 'attack', 'transaction_time': 1643482627}], 'crabada_id_1': 18953, 'crabada_id_2': 18955, 'crabada_id_3': 16969, 'mine_point_modifier': 0, 'crabada_1_photo': '18953.png', 'crabada_2_photo': '18955.png', 'crabada_3_photo': '16969.png', 'defense_crabada_number': 3}]
    return getRemainingTime(mine) < 15000 or mine["winner_team_id"] is not None


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
    return game["status"] == "close"


def getRemainingTime(game: Game) -> int:
    """
    Seconds to the end of the given game
    """
    return int(game["end_time"] - time())


def getRemainingTimeFormatted(game: Game) -> str:
    """
    Hours, minutes and seconds to the end of the given game
    """
    return getPrettySeconds(getRemainingTime(game))


def getNextMineToFinish(games: List[Game]) -> Game:
    """
    Given a list of games, return the mine that is open and
    next to finish; returns None if there are no unfinished games.

    By finished we mean past the 4th hour, regardless of whether
    the reward has been claimed.
    """
    unfinishedGames = [g for g in games if not mineIsFinished(g)]
    return firstOrNone(sorted(unfinishedGames, key=lambda g: g["end_time"]))


def fetchOpenMines(user: User) -> List[Game]:
    """
    Fetch all open mines that were opened by teams
    belonging to the given user
    """

    teamIds = [t["id"] for t in user.getTeams()]

    if not teamIds:
        return []

    openGames = crabadaWeb2Client.listMines(
        {"limit": len(teamIds) * 2, "status": "open", "user_address": user.address}
    )

    return [g for g in openGames if g["team_id"] in teamIds]


def fetchOpenLoots(user: User) -> List[Game]:
    """
    Fetch all mines that are being looted by teams
    belonging to the given user
    """

    teamIds = [t["id"] for t in user.getTeams()]

    if not teamIds:
        return []

    openLoots = crabadaWeb2Client.listMines(
        {"limit": len(teamIds) * 2, "status": "open", "looter_address": user.address}
    )

    return [g for g in openLoots if g["attack_team_id"] in teamIds]
