"""
Settle all loots of a given user
"""

from src.common.logger import logger
from src.common.txLogger import txLogger, logTx
from src.helpers.sms import sendSms
from typing import List, Literal
from src.common.clients import crabadaWeb2Client, crabadaWeb3Client
from eth_typing import Address
from src.helpers.mines import getNextMineToFinish, getRemainingTimeFormatted, mineIsSettled
from src.libs.CrabadaWeb2Client.types import Game

def closeLoots(userAddress: Address) -> int:
    """
    Settle all open loot games that can be settled; return
    the number of closed loots.

    TODO: implement paging
    """

    openLoots = crabadaWeb2Client.listMines({
        "limit": 200,
        "status": "open",
        "looter_address": userAddress})
    
    # Games with a reward to claim
    settledGames = [ g for g in openLoots if mineIsSettled(g) ]

    # Print a useful message in case there aren't finished games 
    if not settledGames:
        logger.info(f'No loots to close for user {str(userAddress)}')
        return 0

    nClosedLoots = 0

    # Close the settled loots
    for g in settledGames:
        gameId = g['game_id']
        logger.info(f'Closing loot {gameId}...')
        txHash = crabadaWeb3Client.settleGame(gameId)
        txLogger.info(txHash)
        txReceipt = crabadaWeb3Client.getTransactionReceipt(txHash)
        logTx(txReceipt)
        if txReceipt['status'] != 1:
            logger.error(f'Error closing loot {gameId}')
            sendSms(f'Crabada: ERROR closing loot > {txHash}')
        else:
            nClosedLoots += 1
            logger.info(f'Loot {gameId} closed correctly')
    
    return nClosedLoots