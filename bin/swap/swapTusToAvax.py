#!/usr/bin/env python3
"""
script to swap TUS to avax via pangolin

Usage:
    python3 -m bin.swap.swapTusToAvax <amount of tus>

"""


from typing import cast
from web3 import Web3

from src.helpers.general import secondOrNone, thirdOrNone
from src.models.User import User
from sys import argv
from src.common.logger import logger
from src.swap import swapTusToAvax


userAddress = secondOrNone(argv)
tusAmount = thirdOrNone(argv)

if not userAddress:
    logger.error("Specify a user address")
    exit(1)
if not tusAmount:
    logger.error("Tus amount not specified")
    exit(1)

tusAmountInWei = Web3.toWei(tusAmount, "ether")


swapTusToAvax(User(userAddress), tusAmountInWei)
