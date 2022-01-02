"""Helper functions to handle Crabada games"""

from src.common.logger import logger
from src.common.txLogger import txLogger
from typing import Any
from time import time

from web3.types import BlockData
from src.common.clients import crabadaWeb2Client, crabadaWeb3Client
from eth_typing import Address

from src.common.types import CrabadaGame
from src.libs.CrabadaWeb3Client.CrabadaWeb3Client import CrabadaWeb3Client
from src.libs.Web3Client.Helpers.Debug import printTxInfo

def closeFinishedGames(userAddress: Address) -> int:
    """Close all open games whose end time is due; return
    the number of closed games"""

    openGames = crabadaWeb2Client.listMines({
        "limit": 200,
        "status": "open",
        "user_address": userAddress})
    
    finishedGames = [ g for g in openGames if gameIsFinished(g) ]
    
    if not finishedGames:
        logger.info('No games to close for user ' + str(userAddress))
        return 0
    
    for i, g in enumerate(finishedGames):
        gameId = g['game_id']
        logger.info(f'Closing game {gameId}...')
        txHash = crabadaWeb3Client.closeGame(g['game_id'])
        txLogger.info(txHash)
        tx_receipt = crabadaWeb3Client.w3.eth.wait_for_transaction_receipt(txHash)
        logger.info(f'Game {gameId} closed')
    
    return i+1

def gameIsFinished(game: CrabadaGame) -> bool:
    """Return true if the given game is past its end_time"""
    return game['end_time'] <= time()

def gameIsClosed(game: CrabadaGame) -> bool:
    """Return true if the given game is closed (meaning the
    reward has been claimed"""
    crabadaWeb2Client.getMine(game['game_id'])
    return game['status'] == 'close'
