"""
Helpers to parse and validate the configuration variables
from the environment
"""

from functools import reduce
import typing
from web3 import Web3
from src.common.exceptions import InvalidConfig, MissingConfig
from src.common.types import (
    ConfigTeam,
    StaggeringGroup,
    ConfigUser,
    Tus,
    TeamTask,
)
from src.common.dotenv import (
    getenv,
    parseFloat,
    parseInt,
    parseListOfInts,
    parseListOfStrings,
)
from typing import List, cast, Set
from eth_typing import Address

from src.helpers.general import duplicatesInList, flattenList
from src.helpers.privatekey import get_private_key


def parseGroupOfTeamsConfigs(groupNumber: int, userNumber: int) -> List[ConfigTeam]:
    """
    Build and return the configurations of the teams in the given group
    from the environment.
    """
    userPrefix = f"USER_{userNumber}"
    groupPrefix = f"{userPrefix}_GROUP_{groupNumber}"
    teamsIds = parseListOfInts(f"{groupPrefix}_TEAMS")

    return [
        parseTeamConfig(
            teamPrefix=groupPrefix,
            userPrefix=userPrefix,
            teamId=teamId,
            teamNumber=i + 1,  # numbering of teams in group is relative to group
            groupNumber=groupNumber,
        )
        for i, teamId in enumerate(teamsIds)
    ]


def parseNonGroupedTeamConfig(teamNumber: int, userNumber: int) -> ConfigTeam:
    """
    Build and return the configuration of the given non-grouped team
    from the environment.
    """
    userPrefix = f"USER_{userNumber}"
    teamPrefix = f"{userPrefix}_TEAM_{teamNumber}"

    return parseTeamConfig(
        teamPrefix=teamPrefix,
        userPrefix=userPrefix,
        teamId=parseInt(teamPrefix),
        teamNumber=teamNumber,
        groupNumber=0,  # alone teams are group 0 by default
    )


def parseTeamConfig(
    teamPrefix: str,
    userPrefix: str,
    teamId: int,
    teamNumber: int,
    groupNumber: int,
) -> ConfigTeam:
    """
    Build and return the configuration of the given team from the
    environment.

    Parameters
    ----------
    teamPrefix : str
        The prefix of the team's configuration in .env. For example,
        USER_1_TEAM_1 if it is a single team or USER_1_GROUP_1 if
        it is a team in a group
    userNumber: int
        The prefix of the user's configuration in .env
    teamId : int
        The ID of the team in Crabada
    teamNumber : int
        The number to assign to the team in the configuration dict.
        Use 0 for teams that belong to a group.
    groupNumber: int
        The group the team belongs to. Use 0 for teams that do not
        belong to a group.
    """
    teamConfig: ConfigTeam = {
        "id": teamId,
        "userAddress": cast(Address, getenv(f"{userPrefix}_ADDRESS")),
        "battlePoints": parseInt(f"{teamPrefix}_BATTLE_POINTS"),
        "task": cast(TeamTask, getenv(f"{teamPrefix}_TASK", "mine")),
        "lootStrategies": parseListOfStrings(
            f"{teamPrefix}_LOOT_STRATEGY", ["LowestBp"]
        ),
        "reinforceStrategies": parseListOfStrings(
            f"{teamPrefix}_REINFORCE_STRATEGY", ["HighestBp"]
        ),
        "reinforcementToPick": parseInt(f"{teamPrefix}_REINFORCEMENT_TO_PICK", 1),
        "teamNumber": teamNumber,
        "groupNumber": groupNumber,
    }

    validateTeamConfig(teamConfig, teamNumber, userPrefix)

    return teamConfig


def parseStaggeringGroups(userNumber: int) -> List[StaggeringGroup]:
    staggeringGroups: List[StaggeringGroup] = []
    groupNumber = 1
    while getenv(f"USER_{userNumber}_STAGGER_GROUP_{groupNumber}_TEAMS"):
        teamsIds = set(
            parseListOfInts(f"USER_{userNumber}_STAGGER_GROUP_{groupNumber}_TEAMS")
        )
        staggeringGroups.append(teamsIds)
        groupNumber += 1
    return staggeringGroups


def parseUserConfig(userNumber: int, teams: List[ConfigTeam]) -> ConfigUser:
    """
    Get the configuration of the given user from the environment

    TODO: Use something like Cerberus to make parsing sustainable
    """
    userPrefix = f"USER_{userNumber}"
    address = cast(Address, getenv(f"{userPrefix}_ADDRESS"))
    reinforcementMaxPriceInTus = parseFloat(f"{userPrefix}_REINFORCEMENT_MAX_PRICE", 0)
    if not reinforcementMaxPriceInTus:  # for backward compatibility
        reinforcementMaxPriceInTus = parseFloat(
            f"{userPrefix}_MAX_PRICE_TO_REINFORCE", 0
        )

    userConfig: ConfigUser = {
        "address": address,
        "privateKey": get_private_key(f"{userPrefix}"),
        "reinforcementMaxPriceInTus": cast(Tus, reinforcementMaxPriceInTus),
        "reinforcementMaxPriceInTusWei": Web3.toWei(
            reinforcementMaxPriceInTus, "ether"
        ),
        "reinforcementMaxGasInGwei": parseFloat(
            f"{userPrefix}_REINFORCEMENT_MAX_GAS", float("inf")
        ),
        "mineMaxGasInGwei": parseFloat(f"{userPrefix}_MINE_MAX_GAS", float("inf")),
        "closeMineMaxGasInGwei": parseFloat(
            f"{userPrefix}_CLOSE_MINE_MAX_GAS", float("inf")
        ),
        "closeLootMaxGasInGwei": parseFloat(
            f"{userPrefix}_CLOSE_LOOT_MAX_GAS", float("inf")
        ),
        "teams": [t for t in teams if t["userAddress"] == address],
        "staggeringGroups": parseStaggeringGroups(userNumber),
        "staggeringDelayInMinutes": parseInt(f"{userPrefix}_STAGGER_DELAY", 35),
    }

    validateUserConfig(userConfig, userNumber)

    return userConfig


def validateTeamConfig(team: ConfigTeam, teamNumber: int, userPrefix: str) -> None:
    """
    Raise an exception if there's something wrong with a single
    team config
    """
    if team["task"] not in typing.get_args(TeamTask):
        raise InvalidConfig(
            f"TASK parameter of team {teamNumber} of user '{userPrefix}' must be one of {str(typing.get_args(TeamTask))}, but '{team['task']}' was given"
        )
    if team["reinforcementToPick"] <= 0 or team["reinforcementToPick"] > 100:
        raise InvalidConfig(
            f"REINFORCEMENT_TO_PICK parameter of team {teamNumber} of user '{userPrefix}' must be an integer between 1 a and 100"
        )


def validateUserConfig(user: ConfigUser, userNumber: int) -> None:
    """
    Raise an exception if there's something wrong with a
    single user's config
    """
    if not user["address"]:
        raise MissingConfig(f"User {userNumber} has no ADDRESS parameter given")
    maxPrice = user.get("reinforcementMaxPriceInTus")
    if not maxPrice or maxPrice <= 0:
        raise MissingConfig(
            f"User {userNumber} has no or invalid REINFORCEMENT_MAX_PRICE (must be a value greater than zero)"
        )
    if not user["teams"]:
        raise MissingConfig(f"User {userNumber} has no team configured")


def validateUsersConfigs(users: List[ConfigUser]) -> None:
    """
    Raise an exception if there are inconsistencies between the
    various users' configurations
    """

    if not users:
        raise MissingConfig("Could not find user private key in config")

    # Check for duplicate users
    userAddresses = [u["address"].lower() for u in users]
    duplicates = duplicatesInList(userAddresses)
    if duplicates:
        raise InvalidConfig(
            f"One or more users appear multiple times in configuration file: {duplicates}"
        )

    # Check for duplicate teams
    allTeams = flattenList([u["teams"] for u in users])
    teamsIds = [t["id"] for t in allTeams]
    duplicates = duplicatesInList(teamsIds)
    if duplicates:
        raise InvalidConfig(
            f"One or more teams appear multiple times in configuration file: {duplicates}"
        )
