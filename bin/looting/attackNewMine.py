#!/usr/bin/env python3
"""
Given a mine that has been just created, attack it with the first
available team with sufficine battle points.

Usage:
    python3 -m bin.looting.handleNewMine <userAddress> <mineId> <teamId>

Author:
    @coccoinomane (Twitter)
"""

from src.bot.looting.attackNewMine import attackNewMine
from typing import cast
from eth_typing import Address
from src.helpers.general import secondOrNone, thirdOrNone
from src.models.User import User
from src.common.logger import logger
from sys import argv
from src.common.clients import crabadaWeb2Client

# PARSE
userAddress = cast(Address, secondOrNone(argv))
mineId = int(thirdOrNone(argv) or 0)

# VALIDATE
if not userAddress:
    logger.error("Specify a user address")
    exit(1)

if not User.isRegistered(userAddress):
    logger.error("The given user address is not registered")
    exit(1)

if not mineId:
    logger.error("Specify a valid mine ID to attack")
    exit(1)

# EXECUTE
attacked = attackNewMine(userAddress, mineId)
