#!/usr/bin/env python3
"""
Crabada script to notify user of idle looting teams
for the given user address.

Usage:
    python3 -m bin.looting.notifyTeamsIdle <userAddress>

Author:
    @coccoinomane (Twitter)
"""

from src.bot.looting.notifyTeamsIdle import notifyTeamsIdle
from src.helpers.general import secondOrNone
from src.models.User import User
from src.common.logger import logger
from sys import argv

userAddress = secondOrNone(argv)

if not userAddress:
    logger.error("Specify a user address")
    exit(1)

nClosed = notifyTeamsIdle(User(userAddress))
