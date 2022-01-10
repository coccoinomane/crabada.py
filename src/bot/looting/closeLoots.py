"""
Settle all loots of a given user
"""

from src.common.logger import logger
from src.common.txLogger import txLogger, logTx
from src.helpers.Sms import sendSms
from typing import List, Literal
from src.common.clients import crabadaWeb2Client, crabadaWeb3Client
from eth_typing import Address
from src.helpers.Mines import getNextMineToFinish, getRemainingTimeFormatted, mineIsFinished
from src.libs.CrabadaWeb2Client.types import Game

def closeLoots(userAddress: Address) -> int:
    """
    Settle all open loot games that can be settled; return
    the number of settled games.

    TODO: implement paging
    """

    openLoots = crabadaWeb2Client.listMines({
        "limit": 200,
        "status": "open",
        "looter_address": userAddress})
    
    # Games with a reward to claim
    # TODO: this works for mines, for loots, we need to know time of when settle is possible
    finishedGames = [ g for g in openLoots if mineIsFinished(g) ]

    # Print a useful message in case there aren't finished games 
    if not finishedGames:
        message = f'No loots to close for user {str(userAddress)}'
        nextGameToFinish = getNextMineToFinish(openLoots)
        # TODO: this works for mines, for loots, we need to know time of when settle is possible
        if nextGameToFinish:
            message += f' (next in {getRemainingTimeFormatted(nextGameToFinish)})'
        logger.info(message)
        return 0

    nClosedGames = 0

    # Close the finished games
    for g in finishedGames:
        gameId = g['game_id']
        logger.info(f'Closing game {gameId}...')
        txHash = crabadaWeb3Client.closeGame(gameId)
        txLogger.info(txHash)
        txReceipt = crabadaWeb3Client.getTransactionReceipt(txHash)
        logTx(txReceipt)
        if txReceipt['status'] != 1:
            logger.error(f'Error closing game {gameId}')
            sendSms(f'Crabada: ERROR closing > {txHash}')
        else:
            nClosedGames += 1
            logger.info(f'Game {gameId} closed correctly')
    
    return nClosedGames