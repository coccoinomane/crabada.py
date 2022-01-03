from src.common.types import ConfigContract, ConfigTeam, ConfigUser
from .dotenv import getenv
import os
from typing import List, cast
from eth_typing import Address

# Project directory
rootDir: str = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

# Teams
teams: List[ConfigTeam] = [
    {
        'id': int(getenv('USER_1_TEAM_1')),
        'userAddress': cast(Address, getenv('USER_1_ADDRESS')),
    },
]

# Users
users: List[ConfigUser] = [
    {
        'name': getenv('USER_1_NAME'),
        'address': cast(Address, getenv('USER_1_ADDRESS')),
        'privateKey': getenv('USER_1_PRIVATE_KEY'),
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

# GAS
defaultGas = getenv('DEFAULT_GAS', '200000') # units
defaultGasPrice = getenv('DEFAULT_GAS_PRICE', '25') # gwei

# TWILIO
twilio = {
    "accountSid": getenv('TWILIO_ACCOUNT_SID'),
    "authToken": getenv('TWILIO_AUTH_TOKEN'),
    "from": getenv('TWILIO_FROM_NUMBER'),
    "to": getenv('TWILIO_TO_NUMBERS'),
}
