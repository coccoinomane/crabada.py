"""
Helper functions to close (i.e. claim rewards from) all mines
of a given user
"""

from src.common.logger import logger
from src.common.txLogger import txLogger, logTx
from src.helpers.sms import sendSms
from src.common.clients import crabadaWeb2Client, crabadaWeb3Client
from eth_typing import Address
from src.helpers.mines import (
    getNextMineToFinish,
    getRemainingTimeFormatted,
    mineIsFinished,
)
from src.libs.CrabadaWeb2Client.types import Game


def closeMines(userAddress: Address) -> int:
    """
    Close all open mining games whose end time is due; return
    the number of closed games.

    TODO: implement paging
    """

    openGames = crabadaWeb2Client.listMines(
        {"limit": 200, "status": "open", "user_address": userAddress}
    )

    # Games with a reward to claim
    finishedGames = [g for g in openGames if mineIsFinished(g)]

    # Print a useful message in case there aren't finished games
    if not finishedGames:
        message = f"No mines to close for user {str(userAddress)}"
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
            sendSms(f"Crabada: ERROR closing mine > {txHash}")
        else:
            nClosedGames += 1
            logger.info(f"Mine {gameId} closed correctly")

    return nClosedGames
