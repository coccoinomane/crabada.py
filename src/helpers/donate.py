from typing import Tuple, cast
from src.common.clients import makeCraClient, makeTusClient
from src.common.config import donatePercentage, donateFrequency
from web3.types import TxReceipt, Wei, Nonce
from src.common.constants import eoas
from random import randint
from src.helpers.rewards import getTusAndCraRewardsFromTxReceipt


def shouldDonate() -> bool:
    """
    Determine whether the bot should attempt to send a donation.

    The donation will never be sent unless the user explicitly
    set the DONATE parameter. And even in this case, the donation
    will happen once every ten times, to save gas.
    """
    return (
        donatePercentage is not None
        and donatePercentage > 0.01
        and rollDice(donateFrequency) == 1  # every ten times
    )


def maybeDonate(txReceipt: TxReceipt) -> Tuple[TxReceipt, TxReceipt]:
    """
    If the user expressed the desire to donate to the
    project, do so.

    Returns the amount of the donation as a (TUS, CRA)
    tuple, or (None, None) if no donation has taken
    place.
    """
    if not shouldDonate():
        return None

    return donate(txReceipt, donatePercentage, donateFrequency)


def donate(
    txReceipt: TxReceipt, percentage: float, multiplier: int = 1
) -> Tuple[TxReceipt, TxReceipt]:
    """
    Donate a percentage of the TUS and CRA rewards;
    return a tuple with the transaction receipts.
    """

    # Donation percentage has to be between 0% and 100%
    percentage = max(0, min(100, percentage))

    if not percentage:
        return (None, None)

    (tusDonation, craDonation) = getDonationAmounts(txReceipt, percentage, multiplier)

    # Initialize clients
    tusClient = makeTusClient()
    craClient = makeCraClient()

    # Get nonce
    nonce = tusClient.getNonce()

    # Send TUS donation
    txTus = tusClient.transfer(eoas["project"], tusDonation, nonce)
    tusReceipt = tusClient.getTransactionReceipt(txTus)

    # Update nonce
    nonce = cast(Nonce, nonce + 1)

    # Send CRA donation
    txCra = craClient.transfer(eoas["project"], craDonation, nonce)
    craReceipt = craClient.getTransactionReceipt(txCra)

    return (tusReceipt, craReceipt)


def getDonationAmounts(
    txReceipt: TxReceipt, percentage: float, multiplier: int = 1
) -> Tuple[Wei, Wei]:
    """
    Given a transaction receipt with TUS and CRA rewards (e.g. a
    closeGame or settleGame tx), return the amount to be donated.
    """

    if percentage > 100:
        raise Exception(f"Donation is higher than rewards [percentage={percentage}]")

    (tusReward, craReward) = getTusAndCraRewardsFromTxReceipt(txReceipt)

    tusDonation = int(percentage * tusReward / 100 * multiplier)
    craDonation = int(percentage * craReward / 100 * multiplier)

    return (cast(Wei, tusDonation), cast(Wei, craDonation))


def rollDice(nSides: int) -> int:
    """
    Get a random integer between 1 and nSides
    """
    return randint(1, nSides)
