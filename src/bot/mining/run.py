from time import sleep
from typing import cast
from eth_typing import Address
from src.bot.mining.sendTeamsMining import sendTeamsMining
from src.bot.mining.reinforceDefense import reinforceDefense
from src.bot.mining.closeMines import closeMines
from src.common.dotenv import getenv, parseInt
from src.models.User import User
from src.common.logger import logger
from sys import exit


def run(user: User, sleep_timer: int, sleep_timer_minor: int) -> None:
    """
    Infinite loop that periodically sends available teams mining,
    reinforces them and eventually claimes their rewards, and then
    starts over again.
    """

    while True:
        try:
            nReinforced = reinforceDefense(user)
        except:
            logger.exception("reinforceDefense exception at run.py")

        try:
            nClosed = closeMines(user)
            if nClosed > 0:
                logger.debug(
                    f"Closed mine count is {nClosed}, waiting for {sleep_timer_minor}"
                )
                sleep(sleep_timer_minor)
        except:
            logger.exception("closeMines exception at run.py")

        try:
            nSent = sendTeamsMining(user)
            if nSent > 0:
                logger.debug(
                    f"Started mine count is {nSent}, waiting for {sleep_timer_minor}"
                )
                sleep(sleep_timer_minor)
        except:
            logger.exception("sendTeamsMining exception at run.py")

        logger.debug(f"Waiting for {sleep_timer} seconds.")
        sleep(sleep_timer)
