from time import sleep
from src.bot.mining.sendTeamsMining import sendTeamsMining
from src.bot.mining.reinforceDefense import reinforceDefense
from src.bot.mining.closeMines import closeMines
from src.helpers.general import randomize
from src.models.User import User
from src.common.logger import logger


def run(
    user: User, sleep_timer: int, sleep_timer_minor: int, sleep_randomizer: float = 0
) -> None:
    """
    Infinite loop that periodically sends available teams mining,
    reinforces them and eventually claimes their rewards, and then
    starts over again.

    Parameters
    ----------
    sleep_timer : int
        Interval between each full cycle of mining, reinforcing
        and settling, in seconds (like a cronjob definition)
    sleep_timer_minor : int
        Interval between closing a mine (closeMines) & opening a new
        one (sendTeamsMining), in seconds
    sleep_randomizer : float
        Randomize sleep timers by this factor. For example, a value
        of 0.2 will randomly vary sleep timers by at most 20%.
    """

    while True:
        try:
            nReinforced = reinforceDefense(user)
        except:
            logger.exception("reinforceDefense exception at run.py")

        try:
            nClosed = closeMines(user)
            if nClosed > 0:
                timer = randomize(sleep_timer_minor, sleep_randomizer)
                logger.debug(f"Closed mine count is {nClosed}, waiting for {timer:.2f}")
                sleep(timer)
        except:
            logger.exception("closeMines exception at run.py")

        try:
            nSent = sendTeamsMining(user)
            if nSent > 0:
                timer = randomize(sleep_timer_minor, sleep_randomizer)
                logger.debug(f"Started mine count is {nSent}, waiting for {timer:.2f}")
                sleep(timer)
        except:
            logger.exception("sendTeamsMining exception at run.py")

        timer = randomize(sleep_timer, sleep_randomizer)
        logger.debug(f"Waiting for {timer:.2f} seconds.")
        sleep(timer)
