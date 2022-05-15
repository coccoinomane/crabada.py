#!/usr/bin/env python3
"""
Crabada script to continuosly mine, reinforce and claim rewards
for all mining teams of the given user.

Usage:
    python3 -m bin.mining.run
"""

from typing import cast
from eth_typing import Address
from src.bot.mining.run import run
from src.common.dotenv import getenv, parseInt
from src.models.User import User
from src.common.logger import logger
from src.helpers.general import secondOrNone
from sys import exit, argv

# Provide user via CLI, or will use 1st registered user
userAddress = secondOrNone(argv) or cast(Address, getenv("USER_1_ADDRESS"))

# Interval between each full cycle of mining, reinforcing
# and settling, in seconds (like a cronjob definition)
sleep_timer = parseInt("SLEEP_TIMER", 120)

# Interval between closing a mine (closeMines) & opening a new
# one (sendTeamsMining), in seconds
sleep_timer_minor = parseInt("SLEEP_TIMER_MINOR", 20)

if not userAddress:
    logger.error("Specify a user address")
    exit(1)

run(User(userAddress), sleep_timer, sleep_timer_minor)
