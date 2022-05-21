"""
Settle all loots of a given user
"""

from src.common.logger import logger, logTx
from src.helpers.instantMessage import sendIM
from src.common.clients import makeCrabadaWeb3Client
from src.helpers.mines import (
    fetchOpenLoots,
    mineCanBeSettled,
)
from src.models.User import User
from web3.exceptions import ContractLogicError
from src.helpers.donate import maybeDonate


def closeLoots(user: User) -> int:
    """
    Settle all open loot games that can be settled; return
    the number of closed loots.
    """
    client = makeCrabadaWeb3Client(
        upperLimitForBaseFeeInGwei=user.config["closeLootMaxGasInGwei"]
    )
    settleableMines = [g for g in fetchOpenLoots(user) if mineCanBeSettled(g)]

    if not settleableMines:
        logger.info(f"No loots to close for user {str(user.address)}")
        return 0

    nClosedLoots = 0

    # Close the settled loots
    for g in settleableMines:
        # Close loot
        gameId = g["game_id"]
        logger.info(f"Closing loot {gameId}...")
        try:
            txHash = client.settleGame(gameId)
        except ContractLogicError as e:
            logger.warning(f"Error closing loot {gameId}: {e}")
            sendIM(f"Error closing loot {gameId}: {e}")
            continue

        # Report
        txReceipt = client.getTransactionReceipt(txHash)
        logTx(txReceipt)
        if txReceipt["status"] != 1:
            logger.error(f"Error closing loot {gameId}")
            sendIM(f"Error closing Loot {gameId}")
        else:
            nClosedLoots += 1
            logger.info(f"Loot {gameId} closed correctly")
            sendIM(f"Loot {gameId} closed correctly")
            maybeDonate(game=g, isMining=False)

    return nClosedLoots
