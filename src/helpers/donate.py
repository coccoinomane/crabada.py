from typing import Tuple, cast, List
from src.common.clients import makeCraClient, makeTusClient
from src.common.config import donatePercentage, donateFrequency
from web3.types import TxReceipt, Wei, Nonce
from src.common.constants import eoas
from src.helpers.rewards import getTusAndCraRewardsFromTxReceipt
import os


claimsLogFilepath = "storage/logs/app/claims.log"
"""
Buffer file containing the user's recent claims.

Each line of the file contains the TUS and CRA rewards
claimed by the user during a closeGame or settleGame
transaction.

The file will be deleted after each donation.
"""


def userWantsToDonate() -> bool:
    """
    Return True if the user agreed to donate to
    the project
    """
    return donatePercentage is not None and donatePercentage > 0.01


def shouldDonate(claims: List[List[float]], donateFrequency: int) -> bool:
    """
    Return True if it is time to donate.

    The principle is simple: we donate only if the user
    claimed X times since his/her last donation, where
    X is given by the 'donateFrequency' parameter.
    """

    return len(claims) > 0 and len(claims) == donateFrequency


def maybeDonate(txReceipt: TxReceipt) -> Tuple[TxReceipt, TxReceipt]:
    """
    If the user expressed the desire to donate to the
    project, do so.

    In order to save gas, we donate only once every X times,
    where X is given by the parameter 'donateFrequency'.

    Returns the TUS and CRA transactions as a tuple, or
    (None, None) if donation has not taken place.
    """

    if not userWantsToDonate():
        return (None, None)

    # Log the rewards that the user just claimed
    rewards = getTusAndCraRewardsFromTxReceipt(txReceipt)
    logClaim(rewards)

    # Determine whether it is time to donate
    claims = getClaimsFromLog()
    if not shouldDonate(claims, donateFrequency):
        return (None, None)

    # Reset the timer, and donate
    deleteClaimsLog()
    return donate(claims, donatePercentage)


def donate(claims: List[List[float]], percentage: float) -> Tuple[TxReceipt, TxReceipt]:
    """
    Donate a percentage of the TUS and CRA rewards;
    return a tuple with the transaction receipts.
    """

    percentage = max(0, min(100, percentage))

    if not percentage:
        return (None, None)

    (tusDonation, craDonation) = getDonationAmounts(claims, percentage)

    # Initialize clients
    tusClient = makeTusClient()
    craClient = makeCraClient()

    # Get nonce
    nonce = tusClient.getNonce()

    # Send TUS donation
    txTus = tusClient.transfer(eoas["project"], tusDonation, nonce)
    tusReceipt = tusClient.getTransactionReceipt(txTus)

    # TODO: Continue only if the first tx went through (status == 1)

    # Update nonce
    nonce = cast(Nonce, nonce + 1)

    # Send CRA donation
    txCra = craClient.transfer(eoas["project"], craDonation, nonce)
    craReceipt = craClient.getTransactionReceipt(txCra)

    return (tusReceipt, craReceipt)


def getDonationAmounts(claims: List[List[float]], percentage: float) -> Tuple[Wei, Wei]:
    """
    Given the list of the recent rewards claimed by the user,
    return the amount to be donated, based on the donation
    percentage choosed by the user
    """

    if percentage > 100:
        raise Exception(f"Donation is higher than rewards [percentage={percentage}]")

    tusTotalRewards = sum([line[0] for line in claims])
    craTotalRewards = sum([line[1] for line in claims])

    tusDonation = int(percentage * tusTotalRewards / 100)
    craDonation = int(percentage * craTotalRewards / 100)

    return (cast(Wei, tusDonation), cast(Wei, craDonation))


def logClaim(rewards: Tuple[float, float]) -> None:
    """
    Append a line to the claims file.
    """
    with open(claimsLogFilepath, "a+") as file:
        file.write("%10.5f %10.5f\n" % rewards)


def getClaimsFromLog() -> List[List[float]]:
    """
    Fetch all the rewards that the user claimed since the
    last donation
    """
    claims: List[List[float]] = []

    with open(claimsLogFilepath, "r") as file:
        claims = [[float(x) for x in line.split()] for line in file]

    return claims


def deleteClaimsLog() -> None:
    """
    Delete the claims file; raises an exception if
    the file is not found
    """

    os.remove(claimsLogFilepath)
