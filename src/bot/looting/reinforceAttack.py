"""
Helper functions to reinforce all loots of a given user
"""

from web3.main import Web3
from src.common.exceptions import NoSuitableReinforcementFound
from src.common.logger import logger, logTx
from src.helpers.instantMessage import sendIM
from src.helpers.mines import fetchOpenLoots
from src.helpers.reinforce import looterCanReinforce
from src.common.clients import makeCrabadaWeb3Client
from src.models.User import User
from src.strategies.reinforce.ReinforceStrategyFactory import getBestReinforcement
from time import sleep
from src.common.config import reinforceDelayInSeconds
from web3.exceptions import ContractLogicError
from src.libs.Web3Client.exceptions import TransactionTooExpensive


def reinforceAttack(user: User) -> int:
    """
    Check if any of the teams of the user that are looting can be
    reinforced, and do so if this is the case; return the
    number of borrowed reinforcements.
    """

    # Client with gas control
    client = makeCrabadaWeb3Client(
        upperLimitForBaseFeeInGwei=user.config["reinforcementMaxGasInGwei"]
    )

    # User's loots that can be reinforced
    reinforceableMines = [m for m in fetchOpenLoots(user) if looterCanReinforce(m)]

    if not reinforceableMines:
        logger.info("No loots to reinforce for user " + str(user.address))
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
            txHash = client.reinforceAttack(mineId, crabId, price)
        except (ContractLogicError, TransactionTooExpensive) as e:
            logger.warning(f"Error reinforcing loot {mineId}: {e}")
            sendIM(f"Error reinforcing loot {mineId}: {e}")
            # Wait some time to avoid renting the same crab for different teams
            if len(reinforceableMines) > 1:
                sleep(reinforceDelayInSeconds)
            continue

        # Report
        txReceipt = client.getTransactionReceipt(txHash)
        logTx(txReceipt)
        if txReceipt["status"] != 1:
            logger.error(f"Error reinforcing loot {mineId}")
            sendIM(crabInfoMsg)
            sendIM(f"Error reinforcing loot {mineId}")
        else:
            nBorrowedReinforments += 1
            logger.info(f"Loot {mineId} reinforced correctly")
            sendIM(crabInfoMsg)
            sendIM(f"Loot {mineId} reinforced correctly")

        # Wait some time to avoid renting the same crab for different teams
        if len(reinforceableMines) > 1:
            sleep(reinforceDelayInSeconds)

    return nBorrowedReinforments
