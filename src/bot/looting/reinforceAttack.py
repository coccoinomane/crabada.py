"""
Helper functions to reinforce all loots of a given user
"""

from web3.main import Web3
from src.common.exceptions import CrabBorrowPriceTooHigh
from src.common.logger import logger
from src.common.txLogger import txLogger, logTx
from src.helpers.Reinforce import minerCanReinforce
from src.helpers.Sms import sendSms
from src.common.clients import crabadaWeb2Client, crabadaWeb3Client
from eth_typing import Address
from src.models.User import User
from src.strategies.StrategyFactory import getBestReinforcement

def reinforceAttack(looterAddress: Address) -> int:
    """
    Check if any of the teams of the user that are looting can be
    reinforced, and do so if this is the case; return the
    number of borrowed reinforcements.
    
    TODO: implement paging
    """
    
    user = User(looterAddress)
    openLoots = crabadaWeb2Client.listMyOpenLoots(looterAddress)
    reinforceableMines = [ m for m in openLoots if minerCanReinforce(m) ]
    if not reinforceableMines:
        logger.info('No loots to reinforce for user ' + str(looterAddress))
        return 0

    # Reinforce the mines
    nBorrowedReinforments = 0
    for mine in reinforceableMines:

        # Find best reinforcement crab to borrow
        mineId = mine['game_id']
        maxPrice = user.config['maxPriceToReinforceInTus']
        strategyName = user.getTeamConfig(mine['team_id']).get('reinforceStrategyName')
        try:
            crab = getBestReinforcement(looterAddress, mine, maxPrice)
        except CrabBorrowPriceTooHigh:
            logger.warning(f"Price of crab is {Web3.fromWei(crab['price'], 'ether')} TUS which exceeds the user limit of {maxPrice} [strategyName={strategyName}]")
            continue
        if not crab:
            logger.warning(f"Could not find a crab to lend for mine {mineId} [strategyName={strategyName}]")
            continue

        crabId = crab['crabada_id']
        price = crab['price']
        logger.info(f"Borrowing crab {crabId} for mine {mineId} at {Web3.fromWei(price, 'ether')} TUS... [strategy={strategyName}, BP={crab['battle_point']}, MP={crab['mine_point']}]")

        # Borrow the crab
        txHash = crabadaWeb3Client.reinforceAttack(mineId, crabId, price)
        txLogger.info(txHash)
        txReceipt = crabadaWeb3Client.getTransactionReceipt(txHash)
        logTx(txReceipt)
        if txReceipt['status'] != 1:
            sendSms(f'Crabada: ERROR reinforcing > {txHash}')
            logger.error(f'Error reinforcing mine {mineId}')
        else:
            nBorrowedReinforments += 1
            logger.info(f"Mine {mineId} reinforced correctly")
            
    return nBorrowedReinforments