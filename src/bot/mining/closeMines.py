"""
Helper functions to close (i.e. claim rewards from) all mines
of a given user
"""

from src.common.logger import logger
from src.common.txLogger import txLogger, logTx
from src.helpers.sms import sendSms
from src.helpers.instantMessage import sendIM
from src.common.clients import crabadaWeb3Client
from src.helpers.mines import (
    fetchOpenMines,
    getNextMineToFinish,
    getRemainingTimeFormatted,
    mineIsFinished,
)
from src.models.User import User


def closeMines(user: User) -> int:
    """
    Close all open mining games whose end time is due; return
    the number of closed games.
    """

    openGames = fetchOpenMines(user)
    finishedGames = [g for g in openGames if mineIsFinished(g)]

    # Print a useful message in case there aren't finished games
    if not finishedGames:
        message = f"No mines to close for user {str(user.address)}"
        nextGameToFinish = getNextMineToFinish(openGames)
        if nextGameToFinish:
            message += f" (next in {getRemainingTimeFormatted(nextGameToFinish)})"
        logger.info(message)
        return 0

    nClosedGames = 0

    # Close the finished games
    for g in finishedGames:
        gameId = g["game_id"]
        logger.info(f"Closing mine {gameId}...")
        txHash = crabadaWeb3Client.closeGame(gameId)
        txLogger.info(txHash)
        txReceipt = crabadaWeb3Client.getTransactionReceipt(txHash)
        logTx(txReceipt)
        if txReceipt["status"] != 1:
            logger.error(f"Error closing mine {gameId}")
            sendSms(f"Crabada: Error closing mine {gameId}")
            sendIM(f"Error closing mine {gameId}")
        else:
            nClosedGames += 1
            logger.info(f"Mine {gameId} closed correctly")
            sendIM(f"Mine {gameId} closed correctly")

    return nClosedGames
