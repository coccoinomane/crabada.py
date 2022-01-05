#!/usr/bin/env python3
"""Crabada script to reinforce all teams of the given
user that are currently mining.

Usage:
    python3 -m bin.reinforce

Author:
    @coccoinomane (Twitter)
"""

from src.helpers.Games import reinforceWhereNeeded
from src.helpers.General import secondOrNone
from src.helpers.Users import isRegistered
from src.common.logger import logger
from sys import argv

from src.common.logger import logger
from src.common.txLogger import txLogger

userAddress = secondOrNone(argv)

if not userAddress:
    logger.error('Specify a user address')
    exit(1)

if not isRegistered(userAddress):
    logger.error('The given user address is not registered')
    exit(1)    

nReinforced = reinforceWhereNeeded(userAddress)
