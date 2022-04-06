#!/usr/bin/env python3
"""
Crabada script to reinforce all mining teams of the given user

Usage:
    python3 -m bin.mining.reinforceDefense <userAddress>

Author:
    @coccoinomane (Twitter)
"""

from src.bot.mining.reinforceDefense import reinforceDefense
from src.helpers.general import secondOrNone
from src.models.User import User
from src.common.logger import logger
from sys import argv

userAddress = secondOrNone(argv)

if not userAddress:
    logger.error("Specify a user address")
    exit(1)

nReinforced = reinforceDefense(User(userAddress))
