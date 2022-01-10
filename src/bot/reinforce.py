"""
Helper functions to reinforce all mines of a given user
"""

from web3.main import Web3
from src.common.exceptions import CrabBorrowPriceTooHigh
from src.common.logger import logger
from src.common.txLogger import txLogger, logTx
from src.helpers.Reinforce import minerCanReinforce
from src.helpers.Sms import sendSms
from src.common.clients import crabadaWeb2Client, crabadaWeb3Client
from eth_typing import Address
from src.helpers.Users import getUserConfig
from src.strategies.reinforce.HighestMpStrategy import HighestMpStrategy

def reinforceWhereNeeded(userAddress: Address) -> int:
    """Check if any of the mining teams of the user can be
    reinforced, and do so if this is the case; return the
    number of borrowed reinforcements
    
    TODO: implement paging
    TODO: implement lending strategies other than cheapest crab"""
    
    user = getUserConfig(userAddress)
    openMines = crabadaWeb2Client.listMyOpenMines(userAddress)
    reinforceableMines = [ m for m in openMines if minerCanReinforce(m) ]
    if not reinforceableMines:
        logger.info('No mines to reinforce for user ' + str(userAddress))
        return 0

    # Reinforce the mines
    nBorrowedReinforments = 0
    for mine in reinforceableMines:

        mineId = mine['game_id']

        # Find best reinforcement crab to borrow
        maxPrice = getUserConfig(userAddress).get('maxPriceToReinforceInTus')

        strategy: HighestMpStrategy = HighestMpStrategy(crabadaWeb2Client).setParams(mine, maxPrice)
        # strategy: HighestBpStrategy = HighestBpStrategy(crabadaWeb2Client).setParams(mine, maxPrice)

        try:
            reinforcementCrab = strategy.getCrab()
        except CrabBorrowPriceTooHigh:
            logger.warning(f"Price of crab is {Web3.fromWei(price, 'ether')} TUS which exceeds the user limit of {user['maxPriceToReinforceInTus']}")
            continue
        if not reinforcementCrab:
            logger.warning(f"Could not find a crab to lend for mine {mineId}")
            continue
        crabId = reinforcementCrab['crabada_id']
        price = reinforcementCrab['price']
        logger.info(f"Borrowing crab {crabId} for mine {mineId} at {Web3.fromWei(price, 'ether')} TUS...")

        # Borrow the crab
        txHash = crabadaWeb3Client.reinforceDefense(mineId, crabId, price)
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