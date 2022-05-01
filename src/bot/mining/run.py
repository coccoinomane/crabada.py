from time import sleep
from src.bot.mining.sendTeamsMining import sendTeamsMining
from src.bot.mining.reinforceDefense import reinforceDefense
from src.bot.mining.closeMines import closeMines

from src.common.dotenv import getenv, parseInt
from src.models.User import User
from src.common.logger import logger
from sys import exit

# use USER_1_ADDRESS as userAddress parameter
userAddress = getenv("USER_1_ADDRESS")

# Like a cronjob definiton,
sleep_timer = parseInt("SLEEP_TIMER", 120)

# we usually can't call sendTeamsMining immediately after closeMines
# but waiting for full 120 seconds a bit too much.
# introduced a second sleep parameter for this reason.
sleep_timer_minor = parseInt("SLEEP_TIMER_MINOR", 20)

if not userAddress:
    logger.error("Specify a user address")
    exit(1)

if not User.isRegistered(userAddress):
    logger.error("The given user address is not registered")
    exit(1)


while True:

    try:
        nReinforced = reinforceDefense(User(userAddress))
    except:
        logger.exception("reinforceDefense exception at run.py")

    try:
        nClosed = closeMines(User(userAddress))
        if nClosed > 0:
            logger.debug(
                f"Closed mine count is {nClosed}, waiting for {sleep_timer_minor}"
            )
            sleep(sleep_timer_minor)
    except:
        logger.exception("closeMines exception at run.py")

    try:
        nSent = sendTeamsMining(User(userAddress))
        if nSent > 0:
            logger.debug(
                f"Started mine count is {nSent}, waiting for {sleep_timer_minor}"
            )
            sleep(sleep_timer_minor)
    except:
        logger.exception("sendTeamsMining exception at run.py")

    logger.debug(f"Waiting for {sleep_timer} seconds.")
    sleep(sleep_timer)
