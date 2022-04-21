"""
Define global configuration variables from reading the
environment
"""

from src.common.exceptions import MissingConfig
from src.common.types import (
    ConfigTeam,
    ConfigUser,
)
from src.common.dotenv import getenv, parseBool, parseInt, parsePercentage
from typing import Any, Dict, List
from src.helpers.config import (
    parseGroupOfTeamsConfigs,
    parseNonGroupedTeamConfig,
    parseUserConfig,
    validateUsersConfigs,
)

#################
# Users config
#################

users: List[ConfigUser] = []
userNumber = 1
while getenv(f"USER_{userNumber}_PRIVATE_KEY"):
    teams: List[ConfigTeam] = []
    # Parse teams that are not grouped
    teamNumber = 1
    while getenv(f"USER_{userNumber}_TEAM_{teamNumber}"):
        teams.append(parseNonGroupedTeamConfig(teamNumber, userNumber))
        teamNumber += 1
    # Parse teams in groups
    groupNumber = 1
    while getenv(f"USER_{userNumber}_GROUP_{groupNumber}_TEAMS"):
        teams += parseGroupOfTeamsConfigs(groupNumber, userNumber)
        groupNumber += 1
    # Parse other configs of user
    users.append(parseUserConfig(userNumber, teams))
    userNumber += 1

validateUsersConfigs(users)

##################
# General options
##################

nodeUri = getenv("WEB3_NODE_URI")
reinforceDelayInSeconds = parseInt("REINFORCE_DELAY_IN_SECONDS", 30)
donatePercentage = parsePercentage("DONATE_PERCENTAGE", 0)
donateFrequency = parseInt("DONATE_FREQUENCY", 10)

##################
# Notifications
##################

telegram: Dict[str, Any] = {
    "enable": parseBool("TELEGRAM_ENABLE", False),
    "apiKey": getenv("TELEGRAM_API_KEY"),
    "chatId": getenv("TELEGRAM_CHAT_ID"),
}

notifications: Dict[str, Any] = {
    "instantMessage": {
        "enable": parseBool("NOTIFICATION_IM", False),
    },
}
