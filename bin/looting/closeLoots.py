#!/usr/bin/env python3
"""
Crabada script to close and claim rewards for all settled loots
for the given user address.

Usage:
    python3 -m bin.looting.closeLoots <userAddress>

Author:
    @coccoinomane (Twitter)
"""

from src.bot.looting.closeLoots import closeLoots
from src.helpers.general import secondOrNone
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

nClosed = closeLoots(userAddress)