from src.common.logger import logger
from src.helpers.instantMessage import sendIM
from src.helpers.teams import fetchAvailableTeamsForTask
from src.models.User import User


def notifyTeamsIdle(user: User) -> int:
    """
    Notify the user if he/she has teams with the 'loot'
    task sitting idle; returns the number of idle teams.
    """

    # Get ids of idle teams
    ids = [str(t["team_id"]) for t in fetchAvailableTeamsForTask(user, "loot")]
    if not ids:
        return 0

    # Notify user
    msg = f"You have teams sitting idle, go loot 🦀 [ids={', '.join(ids)}]"
    logger.info(msg)
    sendIM(msg, forceSend=True, silent=False)

    return len(ids)
