"""
Send a user's available teams mining
"""

from src.common.logger import logger
from src.common.txLogger import txLogger, logTx
from src.helpers.sms import sendSms
from src.helpers.instantMessage import sendIM
from src.common.clients import crabadaWeb3Client
from src.helpers.teams import fetchAvailableTeamsForTask
from src.models.User import User


def sendTeamsMining(user: User) -> int:
    """
    Send mining the available teams with the 'mine' task.

    Returns the opened mines
    """

    availableTeams = fetchAvailableTeamsForTask(user, "mine")

    if not availableTeams:
        logger.info("No available teams to send mining for user " + str(user.address))
        return 0

    # Send the teams
    nSentTeams = 0
    for t in availableTeams:

        teamId = t["team_id"]
        logger.info(f"Sending team {teamId} to mine...")

        txHash = crabadaWeb3Client.startGame(teamId)
        txLogger.info(txHash)
        txReceipt = crabadaWeb3Client.getTransactionReceipt(txHash)
        logTx(txReceipt)
        if txReceipt["status"] != 1:
            sendSms(f"Crabada: Error sending team {teamId} mining")
            logger.error(f"Error sending team {teamId} mining")
            sendIM(f"Error sending team {teamId} mining")
        else:
            nSentTeams += 1
            logger.info(f"Team {teamId} sent successfully")
            sendIM(f"Team {teamId} sent successfully")

    return nSentTeams
