from typing import List
from src.common.types import TeamTask
from src.libs.CrabadaWeb2Client.types import Team
from src.models.User import User
from src.common.clients import crabadaWeb2Client


def fetchAvailableTeamsForTask(user: User, task: TeamTask) -> List[Team]:
    """
    Fetch available teams from Crabada, and return only those
    that are supposed to perform the given task
    """

    # Teams that are supposed to perform the given task
    ids = [t["id"] for t in user.getTeamsByTask(task)]

    if not ids:
        return []

    # Fetch list of available teams
    availableTeams = crabadaWeb2Client.listTeams(
        user.address, {"is_team_available": 1, "limit": len(ids) * 2, "page": 1}
    )

    # Intersect teams with the task with available teams
    return [t for t in availableTeams if t["team_id"] in ids]
