"""
Send a user's available teams mining
"""

from src.common.logger import logger
from src.common.txLogger import txLogger, logTx
from src.helpers.instantMessage import sendIM
from src.common.clients import makeCrabadaWeb3Client
from src.helpers.teams import fetchAvailableTeamsForTask
from src.models.User import User
from web3.exceptions import ContractLogicError


def notifyTeamsIdle(user: User) -> int:
    """
    Send mining the available teams with the 'mine' task
    Notify the idle teams to the user

    Returns the opened mines
    """
    client = makeCrabadaWeb3Client(
        upperLimitForBaseFeeInGwei=user.config["mineMaxGasInGwei"]
    )
    availableTeams = fetchAvailableTeamsForTask(user, "loot")

    if not availableTeams:
        logger.info("No available teams to send looting for user " + str(user.address))
        return 0

    # Send the teams
    nIdleTeams = 0
    for t in availableTeams:

        # Send team
        teamId = t["team_id"]
        logger.info(f"Team {teamId} is sitting idle! Go start the loot... 🦀")
        sendIM(f"Team {teamId} is sitting idle! Go start the loot... 🦀", forceSend=True, disableNotifications=False);

    return nIdleTeams
