from src.common.logger import logger
from src.common.txLogger import txLogger, logTx
from src.helpers.sms import sendSms
from typing import List, Literal
from src.common.clients import crabadaWeb2Client, crabadaWeb3Client
from eth_typing import Address
from src.helpers.mines import (
    getNextMineToFinish,
    getRemainingTimeFormatted,
    mineIsSettled,
)
from src.libs.CrabadaWeb2Client.types import Game
from src.models.User import User


def attackNewMine(userAddress: Address, mineId: int) -> bool:
    """
    Attack the given mine with the first available team; return
    True if the mine is succesfully attacked
    """

    attacked = False
    for teamConfig in User(userAddress).getTeams():
        teamId = teamConfig["id"]
        logger.info(f"Attacking mine {mineId} with team {teamId}...")
        txHash = crabadaWeb3Client.attack(mineId, teamId)
        txLogger.info(txHash)
        txReceipt = crabadaWeb3Client.getTransactionReceipt(txHash)
        logTx(txReceipt)
        if txReceipt["status"] != 1:
            logger.error(f"Error attackin mine {mineId}")
            sendSms(f"Crabada: ERROR attacking mine > {txHash}")
        else:
            logger.info(f"Mine {mineId} attacked correctly")
            attacked = True

    return attacked
