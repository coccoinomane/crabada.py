"""
Helper functions to reinforce all mines of a given user
"""

from web3.main import Web3
from src.common.exceptions import NoSuitableReinforcementFound
from src.common.logger import logger
from src.common.txLogger import txLogger, logTx
from src.helpers.mines import fetchOpenMines
from src.helpers.reinforce import minerCanReinforce
from src.helpers.instantMessage import sendIM
from src.common.clients import makeCrabadaWeb3Client
from src.models.User import User
from src.strategies.reinforce.ReinforceStrategyFactory import getBestReinforcement
from time import sleep
from src.common.config import reinforceDelayInSeconds, notifications
from web3.exceptions import ContractLogicError
from src.libs.Web3Client.exceptions import TransactionTooExpensive


def reinforceDefense(user: User) -> int:
    """
    Check if any of the teams of the user that are mining can be
    reinforced, and do so if this is the case; return the
    number of borrowed reinforcements.
    """

    # Client with gas control
    client = makeCrabadaWeb3Client(
        upperLimitForBaseFeeInGwei=user.config["reinforcementMaxGasInGwei"]
    )

    # User's mines that can be reinforced
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
        try:
            crab = getBestReinforcement(user, mine, maxPrice)
        except NoSuitableReinforcementFound as e:
            logger.warning(f"{e.__class__.__name__}: {e}")
            continue

        # Some strategies might return no reinforcement
        if not crab:
            continue

        crabId = crab["crabada_id"]
        price = crab["price"]
        crabInfoMsg = f"Borrowing crab {crabId} for mine {mineId} at {Web3.fromWei(price, 'ether')} TUS... [BP={crab['battle_point']}, MP={crab['mine_point']}]"
        logger.info(crabInfoMsg)  # TODO: also send to Telegram, asynchronously

        # Borrow the crab
        try:
            txHash = client.reinforceDefense(mineId, crabId, price)
        except (ContractLogicError, TransactionTooExpensive) as e:
            logger.warning(f"Error reinforcing mine {mineId}: {e}")
            sendIM(f"Error reinforcing mine {mineId}: {e}")
            # Wait some time to avoid renting the same crab for different teams
            if len(reinforceableMines) > 1:
                sleep(reinforceDelayInSeconds)
            continue

        # Report
        txLogger.info(txHash)
        txReceipt = client.getTransactionReceipt(txHash)
        logTx(txReceipt)
        if txReceipt["status"] != 1:
            logger.error(f"Error reinforcing mine {mineId}")
            sendIM(f"Error reinforcing mine {mineId}: {crabInfoMsg}.")
        else:
            nBorrowedReinforments += 1
            logger.info(f"Mine {mineId} reinforced correctly")
            if (notifications["instantMessage"]["onReinforce"]):
                sendIM(f"Mine {mineId} reinforced correctly. {crabInfoMsg.replace('Borrowing', 'Borrowed')}")
                
        # Wait some time to avoid renting the same crab for different teams
        if len(reinforceableMines) > 1:
            sleep(reinforceDelayInSeconds)

    return nBorrowedReinforments
