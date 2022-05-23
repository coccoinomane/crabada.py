"""
Helper functions to close (i.e. claim rewards from) all mines
of a given user
"""

from src.common.logger import logger, logTx
from src.helpers.instantMessage import sendIM
from src.common.clients import makeCrabadaWeb3Client
from src.helpers.mines import (
    fetchOpenMines,
    getNextMineToFinish,
    getRemainingTimeFormatted,
    mineIsFinished,
)
from src.models.User import User
from web3.exceptions import ContractLogicError
from src.helpers.donate import maybeDonate


def closeMines(user: User) -> int:
    """
    Close all open mining games whose end time is due; return
    the number of closed games.
    """
    client = makeCrabadaWeb3Client(
        upperLimitForBaseFeeInGwei=user.config["closeMineMaxGasInGwei"]
    )
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

        # Close mine
        gameId = g["game_id"]
        logger.info(f"Closing mine {gameId}...")
        try:
            txHash = client.closeGame(gameId)
        except ContractLogicError as e:
            logger.warning(f"Error closing mine {gameId}: {e}")
            sendIM(f"Error closing mine {gameId}: {e}")
            continue

        # Report
        txReceipt = client.getTransactionReceipt(txHash)
        logTx(txReceipt)
        if txReceipt["status"] != 1:
            logger.error(f"Error closing mine {gameId}")
            sendIM(f"Error closing mine {gameId}")
        else:
            nClosedGames += 1
            logger.info(f"Mine {gameId} closed correctly")
            sendIM(f"Mine {gameId} closed correctly")
            maybeDonate(game=g, isMining=True)

    return nClosedGames
