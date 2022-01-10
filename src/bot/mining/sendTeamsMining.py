"""
Send a user's available teams mining
"""

from src.common.logger import logger
from src.common.txLogger import txLogger, logTx
from src.helpers.Sms import sendSms
from src.common.clients import crabadaWeb2Client, crabadaWeb3Client
from eth_typing import Address

def sendTeamsMining(userAddress: Address) -> int:
    """
    Send all available teams of crabs to mine.
    
    A game/mine will be started for each available team; returns the number
    of games opened.

    TODO: implement paging
    """
    availableTeams = crabadaWeb2Client.listTeams(userAddress, {
        "is_team_available": 1,
        "limit": 200,
        "page": 1})

    if not availableTeams:
        logger.info('No available teams to send mining for user ' + str(userAddress))
        return 0

    # Send the teams
    nSentTeams = 0
    for t in availableTeams:

        teamId = t['team_id']
        logger.info(f'Sending team {teamId} to mine...')

        txHash = crabadaWeb3Client.startGame(teamId)
        txLogger.info(txHash)
        txReceipt = crabadaWeb3Client.getTransactionReceipt(txHash)
        logTx(txReceipt)
        # TODO: log the game that was created
        if txReceipt['status'] != 1:
            sendSms(f'Crabada: ERROR sending > {txHash}')
            logger.error(f'Error sending team {teamId}')
        else:
            nSentTeams += 1
            logger.info(f'Team {teamId} sent succesfully')

    return nSentTeams