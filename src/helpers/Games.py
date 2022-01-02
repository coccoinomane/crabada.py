"""Helper functions to handle Crabada games"""

from typing import Any

from web3.types import BlockData
from common.clients import crabadaWeb2Client, crabadaWeb3Client
from eth_typing import Address

def closeFinishedGames(userAddress: Address) -> None:
    """Close all open games whose end time is due"""

    openGames = crabadaWeb2Client.listMines(userAddress, {"limit": 100, "page": 1, "status": "open"})
    finishedGames = [ g for g in openGames if gameIsFinished(g) ]
    for g in finishedGames:
        txHash = crabadaWeb3Client.closeGame(g.game_id)
        tx_receipt = crabadaWeb3Client.w3.eth.wait_for_transaction_receipt(txHash)

def gameIsFinished(game: dict[str, Any], latestBlock: BlockData = None) -> bool:
    """Return true if the given game is past its end_time"""
    if latestBlock == None:
        latestBlock = crabadaWeb3Client.w3.eth.get_block('latest')
    return game['end_time'] <= latestBlock['number']