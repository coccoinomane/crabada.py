"""
Send a user's available teams looting
"""

from src.common.logger import logger
from src.common.txLogger import txLogger, logTx
from src.helpers.sms import sendSms
from src.common.clients import crabadaWeb2Client, crabadaWeb3Client
from eth_typing import Address
from src.strategies.StrategyFactory import getBestMineToLoot
from src.strategies.loot.LowestBpLootStrategy import LowestBpLootStrategy

def sendTeamsLooting(userAddress: Address) -> int:
    """
    Send all available teams of crabs to loot.
    
    A mine game will be attacked for each available team; returns the
    number of mines attacked.

    TODO: implement paging
    """
    availableTeams = crabadaWeb2Client.listTeams(userAddress, {
        "is_team_available": 1,
        "limit": 200,
        "page": 1})

    if not availableTeams:
        logger.info('No available teams to send looting for user ' + str(userAddress))
        return 0

    # Send the teams
    nAttackedMines = 0
    for t in availableTeams:

        teamId = t['team_id']
        logger.info(f'Sending team {teamId} to loot...')

        # Find best mine to loot
        mine = getBestMineToLoot(userAddress, t)
        if not mine:
            logger.warning(f"Could not find a suitable mine to loot for team {teamId}")
            continue

        # Send the attack tx
        txHash = crabadaWeb3Client.attack(mine['game_id'], teamId)
        txLogger.info(txHash)
        txReceipt = crabadaWeb3Client.getTransactionReceipt(txHash)
        logTx(txReceipt)
        if txReceipt['status'] != 1:
            # sendSms(f'Crabada: ERROR attacking > {txHash}')
            logger.error(f'Error attacking mine {str(mine["game_id"])} with team {teamId}')
        else:
            nAttackedMines += 1
            logger.info(f'Team {teamId} sent succesfully')

    return nAttackedMines