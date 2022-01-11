#!/usr/bin/env python3
"""
Crabada script to reinforce all looting teams of the given user

Usage:
    python3 -m bin.mining.reinforceAttack <userAddress>

Author:
    @coccoinomane (Twitter)
"""

from src.bot.looting.reinforceAttack import reinforceAttack
from src.helpers.General import secondOrNone
from src.models.User import User
from src.common.logger import logger
from sys import argv

userAddress = secondOrNone(argv)

if not userAddress:
    logger.error('Specify a user address')
    exit(1)

if not User.isRegistered(userAddress):
    logger.error('The given user address is not registered')
    exit(1)    

nReinforced = reinforceAttack(userAddress)
