from .dotenv import getenv

# Users
users = [
    {
        'name': getenv('USER_1_NAME'),
        'address': getenv('USER_1_ADDRESS'),
        'privateKey': getenv('USER_1PRIVATE_KEY'),
    },
]

# Teams
crabadaTeams = [
    {
        'id': getenv('USER_1_TEAM_1'),
        'user': getenv('USER_1_ADDRESS'),
    },
]

# RPC
nodeUri = getenv('WEB3_NODE_URI')