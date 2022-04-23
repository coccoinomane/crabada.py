#!/usr/bin/env python3
"""
script to swap CRA to avax via traderjoe

Usage:
    python3 -m bin.traderjoe.swapCraToAvax <ur address> <amount of tus>

"""


from typing import cast
from web3 import Web3

from src.helpers.general import secondOrNone, thirdOrNone
from src.models.User import User
from sys import argv
from src.common.logger import logger
from src.swap import CRA_TO_AVAX_PATH, swapTokenToAvaxTraderJoe

userAddress = secondOrNone(argv)
tusAmount = thirdOrNone(argv)

if not userAddress:
    logger.error("Specify a user address")
    exit(1)
if not tusAmount:
    logger.error("Tus amount not specified")
    exit(1)

tusAmountInWei = Web3.toWei(tusAmount, "ether")

swapTokenToAvaxTraderJoe(User(userAddress), tusAmountInWei, CRA_TO_AVAX_PATH)
