"""Helper functions to handle Crabada games"""

from src.common.logger import logger
from src.common.txLogger import txLogger
from typing import Any
from time import time

from web3.types import BlockData
from src.common.clients import crabadaWeb2Client, crabadaWeb3Client
from eth_typing import Address

from src.common.types import CrabadaGame

def closeFinishedGames(userAddress: Address) -> None:
    """Close all open games whose end time is due"""

    openGames = crabadaWeb2Client.listMines({
        "limit": 200,
        "status": "open",
        "user_address": userAddress})
    
    finishedGames = [ g for g in openGames if gameIsFinished(g) ]
    for g in finishedGames:
        gameId = g['game_id']
        # txHash = crabadaWeb3Client.closeGame(g['game_id'])
        # txLogger.debug(txHash)
        # tx_receipt = crabadaWeb3Client.w3.eth.wait_for_transaction_receipt(txHash)

def gameIsFinished(game: CrabadaGame) -> bool:
    """Return true if the given game is past its end_time"""
    return game['end_time'] <= time()

def gameIsClosed(game: CrabadaGame) -> bool:
    """Return true if the given game is closed (meaning the
    reward has been claimed"""
    crabadaWeb2Client.getMine(game['game_id'])
    return game['status'] == 'close'
