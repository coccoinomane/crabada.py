"""
Helper functions to reinforce all mines of a given user
"""

from web3.main import Web3
from src.common.exceptions import (
    ReinforcementTooExpensive,
    NoSuitableReinforcementFound,
)
from src.common.logger import logger
from src.common.txLogger import txLogger, logTx
from src.helpers.mines import fetchOpenMines
from src.helpers.reinforce import minerCanReinforce
from src.helpers.sms import sendSms
from src.helpers.instantMessage import sendIM
from src.common.clients import crabadaWeb3Client
from src.models.User import User
from src.strategies.reinforce.ReinforceStrategyFactory import getBestReinforcement
from time import sleep
from src.common.config import reinforceDelayInSeconds


def reinforceDefense(user: User) -> int:
    """
    Check if any of the teams of the user that are mining can be
    reinforced, and do so if this is the case; return the
    number of borrowed reinforcements.
    """

    reinforceableMines = [m for m in fetchOpenMines(user) if minerCanReinforce(m)]

    if not reinforceableMines:
        logger.info("No mines to reinforce for user " + str(user.address))
        return 0

    # Reinforce the mines
    nBorrowedReinforments = 0
    for mine in reinforceableMines:

        # Find best reinforcement crab to borrow
        mineId = mine["game_id"]
        maxPrice = user.config["reinforcementMaxPriceInTus"]
        strategyName = user.getTeamConfig(mine["team_id"]).get("reinforceStrategyName")
        try:
            crab = getBestReinforcement(user, mine, maxPrice)
        except (ReinforcementTooExpensive, NoSuitableReinforcementFound) as e:
            logger.warning(e.__class__.__name__ + ": " + str(e))
            continue

        # Some strategies might return no reinforcement
        if not crab:
            continue

        crabId = crab["crabada_id"]
        price = crab["price"]
        crabInfoMsg = f"Borrowing crab {crabId} for mine {mineId} at {Web3.fromWei(price, 'ether')} TUS... [strategy={strategyName}, BP={crab['battle_point']}, MP={crab['mine_point']}]"
        logger.info(crabInfoMsg)  # TODO: also send to Telegram, asynchronously

        # Borrow the crab
        txHash = crabadaWeb3Client.reinforceDefense(mineId, crabId, price)
        txLogger.info(txHash)
        txReceipt = crabadaWeb3Client.getTransactionReceipt(txHash)
        logTx(txReceipt)
        if txReceipt["status"] != 1:
            sendSms(f"Crabada: Error reinforcing mine {mineId}")
            logger.error(f"Error reinforcing mine {mineId}")
            sendIM(crabInfoMsg)
            sendIM(f"Error reinforcing mine {mineId}")
        else:
            nBorrowedReinforments += 1
            logger.info(f"Mine {mineId} reinforced correctly")
            sendIM(crabInfoMsg)
            sendIM(f"Mine {mineId} reinforced correctly")

        # Wait some time to avoid renting the same crab for different teams
        if len(reinforceableMines) > 1:
            sleep(reinforceDelayInSeconds)

    return nBorrowedReinforments
