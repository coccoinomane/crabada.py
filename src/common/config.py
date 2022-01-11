import typing
from web3 import Web3
from src.common.types import ConfigContract, ConfigTeam, ConfigUser, Tus, TeamTask, LootStrategyName, ReinforceStrategyName
from .dotenv import getenv
import os
from typing import List, cast
from src.common.exceptions import InvalidConfig, MissingConfig
from eth_typing import Address

#################
# Parse
#################

# Project directory
rootDir: str = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

# Teams
teams: List[ConfigTeam] = [
    {
        'id': int(getenv('USER_1_TEAM_1')),
        'userAddress': cast(Address, getenv('USER_1_ADDRESS')),
        'task': cast(TeamTask, getenv('USER_1_TEAM_1_TASK', 'mine')),
        'lootStrategyName': cast(LootStrategyName, getenv('USER_1_TEAM_1_LOOT_STRATEGY', 'LowestBp')),
        'reinforceStrategyName': cast(ReinforceStrategyName, getenv('USER_1_TEAM_1_REINFORCE_STRATEGY', 'HighestBp')),
    },
]

# Users
users: List[ConfigUser] = [
    {
        'name': getenv('USER_1_NAME'),
        'address': cast(Address, getenv('USER_1_ADDRESS')),
        'privateKey': getenv('USER_1_PRIVATE_KEY'),
        'maxPriceToReinforceInTus': cast(Tus, int(getenv('USER_1_MAX_PRICE_TO_REINFORCE')) or 0), # in TUS
        'maxPriceToReinforceInTusWei': Web3.toWei(int(getenv('USER_1_MAX_PRICE_TO_REINFORCE') or 0), 'ether'), # in TUS wei
        'teams': [ t for t in teams if t['userAddress'] == cast(Address, getenv('USER_1_ADDRESS')) ]
    },
]

# Contract
contract: ConfigContract = {
    'address': cast(Address, '0x82a85407bd612f52577909f4a58bfc6873f14da8'),
    'abi': rootDir + '/contracts/abi-crabada.json',
}

# RPC
nodeUri = getenv('WEB3_NODE_URI')
chainId = int(getenv('CHAIN_ID'))

# Gas
defaultGas = getenv('DEFAULT_GAS', '200000') # units
defaultGasPrice = getenv('DEFAULT_GAS_PRICE', '25') # gwei

# Twilio
twilio = {
    "accountSid": getenv('TWILIO_ACCOUNT_SID'),
    "authToken": getenv('TWILIO_AUTH_TOKEN'),
}

# Notifications
notifications = {
    "sms": {
        "enable": True if "1" == str(getenv('NOTIFICATION_SMS', '0')) else False,
        "from": getenv('NOTIFICATION_SMS_FROM'),
        "to": getenv('NOTIFICATION_SMS_TO'),
    }
}

#################
# Validate
#################

# Validate teams
for team in teams:
    if team['task'] not in typing.get_args(TeamTask):
        raise InvalidConfig(f"task of team {team['id']} must be one of {str(typing.get_args(TeamTask))}, is '{team['task']}'")
    if team['lootStrategyName'] not in typing.get_args(LootStrategyName):
        raise InvalidConfig(f"lootStrategy of team {team['id']} must be one of {str(typing.get_args(LootStrategyName))}, is '{team['lootStrategyName']}'")
    if team['reinforceStrategyName'] not in typing.get_args(ReinforceStrategyName):
        raise InvalidConfig(f"reinforceStrategy of team {team['id']} must be one of {str(typing.get_args(ReinforceStrategyName))}, is '{team['reinforceStrategyName']}'")

# Validate users
for user in users:
    if not user['address']:
        raise MissingConfig("User has no ADDRESS")
    maxPrice = user.get('maxPriceToReinforceInTus')
    if not maxPrice or maxPrice <= 0:
        raise MissingConfig("User has no or invalid MAX_PRICE_TO_REINFORCE (must be a value greater than zero)")
