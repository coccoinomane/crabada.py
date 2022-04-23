#!/usr/bin/env python3
"""
script to swap CRA to avax via pangolin

Usage:
    python3 -m bin.pangolin.swapCraToAvax <ur address> <amount of CRA>

"""


from typing import cast
from web3 import Web3

from src.helpers.general import secondOrNone, thirdOrNone
from src.models.User import User
from sys import argv
from src.common.logger import logger
from src.swap import CRA_TO_AVAX_PATH, swapTokenToAvaxPangolin

userAddress = secondOrNone(argv)
craAmount = thirdOrNone(argv)

if not userAddress:
    logger.error("Specify a user address")
    exit(1)
if not craAmount:
    logger.error("Cra amount not specified")
    exit(1)

craAmountInWei = Web3.toWei(craAmount, "ether")

swapTokenToAvaxPangolin(User(userAddress), craAmountInWei, CRA_TO_AVAX_PATH)
