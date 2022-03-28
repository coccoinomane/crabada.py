"""
Settle all loots of a given user
"""

from src.common.logger import logger
from src.common.txLogger import txLogger, logTx
from src.helpers.sms import sendSms
from src.common.clients import crabadaWeb3Client
from src.helpers.mines import (
    fetchOpenLoots,
    mineReadyToBeSettled,
)
from src.models.User import User


def closeLoots(user: User) -> int:
    """
    Settle all open loot games that can be settled; return
    the number of closed loots.
    """

    readyToBeSettledGames = [g for g in fetchOpenLoots(user) if mineReadyToBeSettled(g)]

    if not readyToBeSettledGames:
        logger.info(f"No loots to close for user {str(user.address)}")
        return 0

    nClosedLoots = 0

    # Close the settled loots
    for g in readyToBeSettledGames:
        gameId = g["game_id"]
        logger.info(f"Closing loot {gameId}...")
        txHash = crabadaWeb3Client.settleGame(gameId)
        txLogger.info(txHash)
        txReceipt = crabadaWeb3Client.getTransactionReceipt(txHash)
        logTx(txReceipt)
        if txReceipt["status"] != 1:
            logger.error(f"Error closing loot {gameId}")
            sendSms(f"Crabada: ERROR closing loot > {txHash}")
        else:
            nClosedLoots += 1
            logger.info(f"Loot {gameId} closed correctly")

    return nClosedLoots
