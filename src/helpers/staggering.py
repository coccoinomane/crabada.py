from src.libs.CrabadaWeb2Client.types import Team
from src.models.User import User
from src.common.clients import makeCrabadaWeb2Client
from src.common.types import StaggeringGroup, TeamTask, ConfigTeam
from src.common.logger import logger

from datetime import datetime
from typing import List, Dict, Set


def _minutesElapsedSinceMiningStart(team: Team) -> int:
    """
    Returns time in minutes elapsed since given team's last
    mining start date
    """
    try:
        timedelta = datetime.utcnow() - datetime.utcfromtimestamp(
            team["mine_start_time"]
        )
        return int(timedelta.total_seconds() // 60)
    except:
        return 10000  # TODO a bigint default value.


def _fetchTeamsWithElapsedTime(user: User) -> Dict[int, int]:
    """
    Returns a dictionary of team_ids and mining elapsed times.

    Fetches all teams of given user, and calculates the elapsed
    time from the last mining operation start date.
    """
    try:
        allTeams = makeCrabadaWeb2Client().listTeams(
            user.address, {"limit": 100, "page": 1}
        )

        result = {
            team["team_id"]: _minutesElapsedSinceMiningStart(team) for team in allTeams
        }
        return result
    except:
        return {}


def _getMinimumElapsedTime(
    staggeringGroup: StaggeringGroup,
    allTeamsWithMineTimings: Dict[int, int],
    exceptTeamId: int,
) -> int:
    """
    Finds minimum elapsed time since last mining expedition (for
    given staggering-group).

    If there is no team currently mining, returns a big-enough
    default value (currently 10000 minutes).
    """
    minimumElapsedTime = 10000  # TODO a bigint default value.
    for team_id in staggeringGroup:
        if team_id != exceptTeamId:
            value = allTeamsWithMineTimings.get(team_id, minimumElapsedTime)
            if value < minimumElapsedTime:
                minimumElapsedTime = value
    logger.debug(f"StaggeringGroups - _getMinimumElapsedTime: {minimumElapsedTime}")
    return minimumElapsedTime


def _checkTeamForMineTimigs(
    team: Team,
    staggeringGroups: List[StaggeringGroup],
    allTeamsWithMineTimings: Dict[int, int],
    staggeringDelayinMinutes: int,
) -> bool:
    team_id = team["team_id"]
    for staggeringGroup in staggeringGroups:

        if team_id not in staggeringGroup:
            continue

        minimumElapsedTime = _getMinimumElapsedTime(
            staggeringGroup, allTeamsWithMineTimings, team_id
        )

        if minimumElapsedTime < staggeringDelayinMinutes:
            # Fail Fast :)
            # We do not need to check other staggering-groups for this team.
            return False

    return True


def _checkTeamForUniqueGroups(
    team: Team, staggeringGroups: List[StaggeringGroup], filteredTeamIdSet: Set[int]
) -> bool:

    if not filteredTeamIdSet:
        return True

    team_id = team["team_id"]
    for staggeringGroup in staggeringGroups:

        if team_id not in staggeringGroup:
            continue

        res = any(t in filteredTeamIdSet for t in staggeringGroup)
        if res:
            return False
    return True


def filterAvailableTeamsForStaggering(user: User, teams: List[Team]) -> List[Team]:
    """
    Given a list of teams, return only those that are ready to
    be sent according to the staggering schedule
    """
    staggeringGroups = user.getStaggeringGroups()
    staggeringDelayinMinutes = user.getStaggeringDelayInMinutes()

    # if there is no stagger-group definition found,
    # return unmofidied list of teams.
    if not staggeringGroups:
        return teams

    filteredTeams: List[Team] = []
    filteredTeamIdSet: Set[int] = set()

    # cache mine-timings of teams
    allTeamsWithMineTimings = _fetchTeamsWithElapsedTime(user)

    for team in teams:
        if _checkTeamForMineTimigs(
            team, staggeringGroups, allTeamsWithMineTimings, staggeringDelayinMinutes
        ) and _checkTeamForUniqueGroups(team, staggeringGroups, filteredTeamIdSet):
            filteredTeams.append(team)

            # Should allow a single team per staggering-group
            # keep team_id's in a set for faster finds.
            filteredTeamIdSet.add(team["team_id"])
        else:
            logger.debug(f"StaggeringGroups - Team {team['team_id']} is filtered out.")
    return filteredTeams
