import typing
from web3 import Web3
from src.common.types import (
    ConfigTeam,
    ConfigUser,
    Tus,
    TeamTask,
    LootStrategyName,
    ReinforceStrategyName,
)
from .dotenv import getenv, parseFloat, parseInt
from typing import List, cast
from src.common.exceptions import InvalidConfig, MissingConfig
from eth_typing import Address

#################
# Parse
#################

# General options
reinforceDelayInSeconds = parseInt("REINFORCE_DELAY_IN_SECONDS", 30)

# Teams
teams: List[ConfigTeam] = []
teamNumber = 1
while getenv(f"USER_1_TEAM_{teamNumber}"):
    teams.append(
        {
            "id": parseInt(f"USER_1_TEAM_{teamNumber}"),
            "userAddress": cast(Address, getenv("USER_1_ADDRESS")),
            "battlePoints": parseInt(f"USER_1_TEAM_{teamNumber}_BATTLE_POINTS"),
            "task": cast(
                TeamTask, getenv(f"USER_1_TEAM_{teamNumber}_TASK", "mine")
            ),  # not implemented yet
            "lootStrategyName": cast(
                LootStrategyName,
                getenv(f"USER_1_TEAM_{teamNumber}_LOOT_STRATEGY", "LowestBp"),
            ),
            "reinforceStrategyName": cast(
                ReinforceStrategyName,
                getenv(f"USER_1_TEAM_{teamNumber}_REINFORCE_STRATEGY", "HighestBp"),
            ),
        }
    )
    teamNumber += 1

# Users
users: List[ConfigUser] = []
userNumber = 1
while getenv(f"USER_{userNumber}_PRIVATE_KEY"):
    users.append(
        {
            "address": cast(Address, getenv(f"USER_{userNumber}_ADDRESS")),
            "privateKey": getenv(f"USER_{userNumber}_PRIVATE_KEY"),
            "maxPriceToReinforceInTus": cast(
                Tus, parseFloat(f"USER_{userNumber}_MAX_PRICE_TO_REINFORCE") or 0
            ),  # in TUS
            "maxPriceToReinforceInTusWei": Web3.toWei(
                parseFloat(f"USER_{userNumber}_MAX_PRICE_TO_REINFORCE") or 0, "ether"
            ),  # in TUS wei
            "teams": [
                t
                for t in teams
                if t["userAddress"]
                == cast(Address, getenv(f"USER_{userNumber}_ADDRESS"))
            ],
        }
    )
    userNumber += 1

# RPC
nodeUri = getenv("WEB3_NODE_URI")

# Gas
defaultGas = getenv("DEFAULT_GAS", "200000")  # units
defaultGasPrice = getenv("DEFAULT_GAS_PRICE", "25")  # gwei

# Twilio
twilio = {
    "accountSid": getenv("TWILIO_ACCOUNT_SID"),
    "authToken": getenv("TWILIO_AUTH_TOKEN"),
}

# Notifications
notifications = {
    "sms": {
        "enable": True if "1" == str(getenv("NOTIFICATION_SMS", "0")) else False,
        "from": getenv("NOTIFICATION_SMS_FROM"),
        "to": getenv("NOTIFICATION_SMS_TO"),
    }
}

#################
# Validate
#################

# Validate teams
if not teams:
    raise MissingConfig("Could not find team configuration")
for team in teams:
    if team["task"] not in typing.get_args(TeamTask):
        raise InvalidConfig(
            f"The TASK parameter of team {team['id']} must be one of {str(typing.get_args(TeamTask))}, but '{team['task']}' was given"
        )
    if team["lootStrategyName"] not in typing.get_args(LootStrategyName):
        raise InvalidConfig(
            f"The LOOT_STRATEGY parameter of team {team['id']} must be one of {str(typing.get_args(LootStrategyName))}, but '{team['lootStrategyName']}' was given"
        )
    if team["reinforceStrategyName"] not in typing.get_args(ReinforceStrategyName):
        raise InvalidConfig(
            f"The REINFORCE STRATEGY parameter of team {team['id']} must be one of {str(typing.get_args(ReinforceStrategyName))}, but '{team['reinforceStrategyName']}' was given"
        )

# Validate users
if not users:
    raise MissingConfig("Could not find user configuration")
for user in users:
    if not user["address"]:
        raise MissingConfig("No ADDRESS parameter was given for a user")
    maxPrice = user.get("maxPriceToReinforceInTus")
    if not maxPrice or maxPrice <= 0:
        raise MissingConfig(
            "User has no or invalid MAX_PRICE_TO_REINFORCE (must be a value greater than zero)"
        )
