from typing import List, Dict
from src.common.types import TeamTask, ConfigTeam
from src.libs.CrabadaWeb2Client.types import Team
from src.models.User import User
from src.common.clients import makeCrabadaWeb2Client
from src.common.config import staggeringDelayInMinutes

from datetime import datetime


def _minutesElapsedSinceMiningStart(team: Team):
    """returns time since given teams last mining"""
    try:
        timedelta = datetime.utcnow() - datetime.utcfromtimestamp(
            team["mine_start_time"]
        )
        return int(timedelta.total_seconds() // 60)
    except:
        return 0


def _fetchTeamsWithElapsedTime(user: User) -> Dict[int, int]:
    # Fetch list of teams
    allTeams = makeCrabadaWeb2Client().listTeams(
        user.address, {"limit": 100, "page": 1}
    )

    result = {
        team["team_id"]: _minutesElapsedSinceMiningStart(team) for team in allTeams
    }
    return result


def _filterAvailableTeamsForStaggering(
    teams: List[Team],
    configTeams: Dict[int, ConfigTeam],
    teamsWithMineTimings: Dict[int, int],
):
    available_teams: List[Team] = []
    for t in teams:
        team_id = t["team_id"]
        prev_team_id = configTeams[team_id]["staggeringPrevTeamId"]
        if prev_team_id == -1:
            available_teams.append(t)
        elif teamsWithMineTimings.get(prev_team_id, 0) > staggeringDelayInMinutes:
            available_teams.append(t)
    return available_teams


def fetchAvailableTeamsForTask(user: User, task: TeamTask) -> List[Team]:
    """
    Fetch available teams from Crabada, and return only those
    that are supposed to perform the given task
    """

    # Teams that are supposed to perform the given task
    configTeams = {t["id"]: t for t in user.getTeamsByTask(task)}
    if not configTeams:
        return []

    # Fetch list of available teams
    availableTeams = makeCrabadaWeb2Client().listTeams(
        user.address, {"is_team_available": 1, "limit": len(configTeams) * 2, "page": 1}
    )

    # Intersect teams with the task with available teams
    availableTeams = [t for t in availableTeams if t["team_id"] in configTeams]

    teamsWithMineTimings = _fetchTeamsWithElapsedTime(user=user)
    availableTeams = _filterAvailableTeamsForStaggering(
        teams=availableTeams,
        configTeams=configTeams,
        teamsWithMineTimings=teamsWithMineTimings,
    )

    return availableTeams
