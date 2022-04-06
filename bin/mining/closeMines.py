#!/usr/bin/env python3
"""
Crabada script to close and claim rewards for all finished mines
for the given user address.

Usage:
    python3 -m bin.mining.closeGames <userAddress>

Author:
    @coccoinomane (Twitter)
"""

from src.bot.mining.closeMines import closeMines
from src.helpers.general import secondOrNone
from src.models.User import User
from src.common.logger import logger
from sys import argv

userAddress = secondOrNone(argv)

if not userAddress:
    logger.error("Specify a user address")
    exit(1)

nClosed = closeMines(User(userAddress))
