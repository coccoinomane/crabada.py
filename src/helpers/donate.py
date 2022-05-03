from typing import Tuple, cast, List
from src.common.logger import logger
from src.common.dotenv import getenv
from src.common.clients import makeAvalancheClient, makeCraClient, makeTusClient
from src.common.config import donatePercentage, donateFrequency
from web3.types import TxReceipt, Wei, Nonce
from src.common.constants import eoas
from src.helpers.instantMessage import sendIM
from src.helpers.rewards import getTusAndCraRewardsFromTxReceipt
from src.helpers.price import tusToWei, craToWei, weiToCra, weiToTus
import os


claimsLogFilepath = os.path.join(
    getenv("STORAGE_FOLDER", "storage"), "logs/app", "claims.log"
)
os.makedirs(os.path.dirname(claimsLogFilepath), exist_ok=True)

"""
Log file containing the user's recent claims.

Each line of the file contains the TUS and CRA rewards
claimed by the user during the most recent closeGame
and settleGame transactions.

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
    return (
        userWantsToDonate() and len(claims) > 0 and len(claims) % donateFrequency == 0
    )


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
        logger.warning(getDonateMessage())
        sendIM(getDonateMessage())
        return (None, None)

    # Log the rewards that the user just claimed
    tusRewardInWei, craRewardInWei = getTusAndCraRewardsFromTxReceipt(txReceipt)
    logClaim((weiToTus(tusRewardInWei), weiToCra(craRewardInWei)))

    # Determine whether it is time to donate
    claims = getClaimsFromLog()
    if not shouldDonate(claims, donateFrequency):
        return (None, None)

    # The donation shall consider only the most recent claims
    recentClaims = claims[-donateFrequency:]

    # Reset the counter, for good measure
    deleteClaimsLog()

    # Donate
    return donate(recentClaims, donatePercentage)


def donate(
    recentClaims: List[List[float]], percentage: float
) -> Tuple[TxReceipt, TxReceipt]:
    """
    Donate a percentage of the TUS and CRA rewards from the
    given claims.

    Return a tuple with the transaction receipts.
    """

    # Make sure the % is within bounds
    percentage = max(0, min(100, percentage))
    if not percentage:
        return (None, None)

    # How much should we donate?
    (tusDonation, craDonation) = getDonationAmounts(recentClaims, percentage)

    # Initialize nonce and receipts
    nonce = makeAvalancheClient().getNonce()
    tusReceipt, craReceipt = None, None

    # Donate TUS
    if tusDonation:
        try:
            tusClient = makeTusClient()
            txTus = tusClient.transfer(eoas["project"], tusDonation, nonce)
            tusReceipt = tusClient.getTransactionReceipt(txTus)
            if tusReceipt["status"] != 1:
                logger.error(
                    f"Error from TUS donation [tx={txTus}, status={tusReceipt['status']}"
                )
            nonce = cast(Nonce, nonce + 1)
        except Exception as e:
            logger.error(f"Could not send TUS donation > {e}")

    # Donate CRA
    if craDonation:
        try:
            craClient = makeCraClient()
            txCra = craClient.transfer(eoas["project"], craDonation, nonce)
            craReceipt = craClient.getTransactionReceipt(txCra)
            if craReceipt["status"] != 1:
                logger.error(
                    f"Error from CRA donation [tx={txCra}, status={craReceipt['status']}"
                )
        except Exception as e:
            logger.error(f"Could not send CRA donation > {e}")

    return (tusReceipt, craReceipt)


def getDonationAmounts(claims: List[List[float]], percentage: float) -> Tuple[Wei, Wei]:
    """
    Given the list of reward claims by the user, return the amount
    to be donated in Wei, based on the donation percentage chosen
    by the user
    """
    if percentage > 100:
        raise Exception(f"Donation is higher than rewards [percentage={percentage}]")

    tusTotalRewards = sum([line[0] for line in claims])
    craTotalRewards = sum([line[1] for line in claims])

    tusDonation = percentage * tusTotalRewards / 100
    craDonation = percentage * craTotalRewards / 100

    return (tusToWei(tusDonation), craToWei(craDonation))


def logClaim(rewards: Tuple[float, float]) -> None:
    """
    Append a line to the claims file
    """
    with open(claimsLogFilepath, "a+") as file:
        file.write("%10.5f %10.5f\n" % rewards)


def getClaimsFromLog() -> List[List[float]]:
    """
    Fetch all the reward claims in the file log
    """
    try:
        with open(claimsLogFilepath, "r") as file:
            return [[float(x) for x in line.split()] for line in file]
    except FileNotFoundError:
        return []


def deleteClaimsLog() -> None:
    """
    Delete the claims file
    """
    try:
        os.remove(claimsLogFilepath)
    except FileNotFoundError:
        pass


def getDonateMessage() -> str:
    return """
🦀  🦀  🦀

Building this bot requires time and passion.
Please consider expressing your gratitude
by donating a small % of your rewards :-)

To donate, write DONATE_PERCENTAGE=3%
in your .env file; this message will
disappear regardless of the amount that
you donate 🙂

Thank you!

🙏  ❤️  🙏
"""
