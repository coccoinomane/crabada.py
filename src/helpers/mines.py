"""
Helper functions to handle Crabada mines / games
"""

from typing import List
from src.helpers.dates import getPrettySeconds
from time import time
from src.common.clients import makeCrabadaWeb2Client
from src.helpers.general import firstOrNone
from src.libs.CrabadaWeb2Client.types import Game, GameProcess
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


def mineCanBeSettled(mine: Game) -> bool:
    """
    Return True if the given game is ready to be settled
    """
    return (
        attackIsOver(mine)
        and not mineIsSettled(mine)  # can't settle if already settled
        and getElapsedTime(mine) > 3600  # can't settle before one hour since start
    )


def attackIsOver(mine: Game) -> bool:
    """
    Return true if the given mine has been attacked and if no
    further reinforcement can be added.

    The latter happens in several occasions:
    - The 30-minute reinforce window has passed without either the
      miner or the looter reinforcing.
    - Both the miner and the looter have already reinforced twice.
    - A looter attacked a miner with more BPs (suicide loot)
    """
    return mineHasBeenAttacked(mine) and (
        getElapsedTimeSinceLastAction(mine) > 1800  # reinforce window over
        or (getTimesMinerReinforced(mine) == 2 and getTimesLooterReinforced(mine) == 2)
        or isSuicideAttack(mine)
    )


def isSuicideAttack(mine: Game) -> bool:
    """
    TO BE IMPLEMENTED: Requires factional advantage.

    Return true if the given mine was attacked by a looter
    with less BPs than the miner.

    We call it a suicide attack because the looter instantly
    loses without the chance to reinforce
    """
    return False


def minerIsWinning(mine: Game) -> bool:
    """
    Return true if the miner is currently winning or if it has won
    """
    return mine["attack_point"] <= mine["defense_point"]


def looterIsWinning(mine: Game) -> bool:
    """
    Return true if the looter is currently winning or if it has won
    """
    return mine["attack_point"] > mine["defense_point"]


def mineIsWaitToSettle(mine: Game) -> bool:
    """
    Return true if the given mine is in the state "Wait to settle",
    meaning the attack sequence is over but the looter still has to
    wait a bit before settling.

    NB: If the looter loses, the Crabada UI shows the "Finished" badge
    instead of the "Wait to settle" one. In this case, the function will
    still return True because the looter will still need to settle.
    """
    return (
        attackIsOver(mine)
        and not mineIsSettled(mine)  # can't settle if already settled
        and getElapsedTime(mine) <= 3600  # can't settle before one hour since start
    )


def mineIsFinished(game: Game) -> bool:
    """
    Return true if the given game is past its end_time
    """
    return getRemainingTime(game) <= 0


def mineIsClosed(game: Game) -> bool:
    """
    Return true if the given game is closed, meaning the
    reward have been claimed.
    """
    return game["status"] == "close"


def mineIsSettled(game: Game) -> bool:
    """
    Return true if the given game is settled, meaning
    either the looter has settled on his own or the game
    was closed by the miner
    """
    return len([p for p in game["process"] if p["action"] == "settle"]) > 0


def getRemainingTime(game: Game) -> int:
    """
    Seconds to the end of the given game
    """
    return max(0, int(game["end_time"] - time()))


def getElapsedTime(game: Game) -> int:
    """
    Seconds since the start of the given game
    """
    return int(time() - game["start_time"])


def getRemainingTimeFormatted(game: Game) -> str:
    """
    Hours, minutes and seconds to the end of the given game
    """
    return getPrettySeconds(getRemainingTime(game))


def getElapsedTimeFormatted(game: Game) -> str:
    """
    Hours, minutes and seconds since the start of the given game
    """
    return getPrettySeconds(getElapsedTime(game))


def getRemainingTimeBeforeSettle(mine: Game) -> int:
    """
    Seconds before the given mine will be ready to be settled.

    The output makes sense only if the attack sequence is over,
    which you can check via attackIsOver()
    """
    return max(0, 3600 - getElapsedTime(mine))


def getRemainingTimeBeforeSettleFormatted(mine: Game) -> str:
    """
    Hours, minutes and seconds to the time when the mine will
    be ready to be settled
    """
    return getPrettySeconds(getRemainingTimeBeforeSettle(mine))


def getTimesLooterReinforced(mine: Game) -> int:
    """
    Number of times the looter has reinforced so far
    """
    return len([x for x in mine["process"] if x["action"] == "reinforce-attack"])


def getTimesMinerReinforced(mine: Game) -> int:
    """
    Number of times the miner has reinforced so far
    """
    return len([x for x in mine["process"] if x["action"] == "reinforce-defense"])


def getNextMineToFinish(games: List[Game]) -> Game:
    """
    Given a list of games, return the mine that is open and
    next to finish; returns None if there are no unfinished games.

    By finished we mean past the 4th hour, regardless of whether
    the reward has been claimed.
    """
    unfinishedGames = [g for g in games if not mineIsFinished(g)]
    return firstOrNone(sorted(unfinishedGames, key=lambda g: g["end_time"]))


def getLastAction(mine: Game) -> GameProcess:
    """
    Return the last action performed to the mine, together
    with its execution time
    """
    return mine["process"][-1]


def getElapsedTimeSinceLastAction(mine: Game) -> int:
    """
    Seconds since the last action performed to the mine
    """
    lastAction = getLastAction(mine)
    return int(time() - lastAction["transaction_time"])


def fetchOpenMines(user: User) -> List[Game]:
    """
    Fetch all open mines that were opened by teams
    belonging to the given user
    """

    teamIds = [t["id"] for t in user.getTeams()]

    if not teamIds:
        return []

    # 2022-05-15 quick fix for issue#107
    # Don't let the limit parameter go above 100 (hard limit of crabada-api)
    limit = min(len(teamIds) * 2, 100)

    openGames = makeCrabadaWeb2Client().listMines(
        {"limit": limit, "status": "open", "user_address": user.address}
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

    openLoots = makeCrabadaWeb2Client().listMines(
        {"limit": len(teamIds) * 2, "status": "open", "looter_address": user.address}
    )

    return [g for g in openLoots if g["attack_team_id"] in teamIds]
