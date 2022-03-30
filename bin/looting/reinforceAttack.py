#!/usr/bin/env python3
"""
Crabada script to reinforce all looting teams of the given user

Usage:
    python3 -m bin.looting.reinforceAttack <userAddress>

Author:
    @coccoinomane (Twitter)
"""

from src.bot.looting.reinforceAttack import reinforceAttack
from src.helpers.general import secondOrNone
from src.models.User import User
from src.common.logger import logger
from sys import argv

userAddress = secondOrNone(argv)

if not userAddress:
    logger.error("Specify a user address")
    exit(1)

nReinforced = reinforceAttack(User(userAddress))
