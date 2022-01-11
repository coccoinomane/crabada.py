#!/usr/bin/env python3
"""Crabada script to close all settled loots for
the given user address.

Usage:
    python3 -m bin.closeLoots

Author:
    @coccoinomane (Twitter)
"""

from src.bot.looting.closeLoots import closeLoots
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

nClosed = closeLoots(userAddress)