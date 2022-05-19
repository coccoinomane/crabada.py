from typing import Iterable, Tuple, cast
from eth_typing import Address
from web3.types import TxReceipt, EventData, Wei
from src.common.clients import makeSwimmerCraClient
from src.common.constants import tokens
from src.helpers.general import firstOrNone

"""
Anything related to TUS and CRA rewards
"""

tusToCraRatio: int = 27
"""
Ratio between the amount of TUS rewarded and the amount
of CRA rewarded
"""


def getTusAndCraRewardsFromTxReceipt(txReceipt: TxReceipt) -> Tuple[Wei, Wei]:
    """
    Given a receipt from a closeGame or settleGame transaction,
    return a tuple with the rewards in TUS and CRA, respectively,
    in Wei.

    If the tx does not contain either TUS or CRA rewards, the return
    tuple will contain None in either position.
    """

    # Return any ERC20 token transfer in the TX
    logs: Iterable[EventData] = (
        makeSwimmerCraClient().contract.events.Transfer().processReceipt(txReceipt)
    )

    craAmount: Wei = firstOrNone(
        [
            l["args"]["value"]
            for l in logs
            if cast(Address, l["address"].lower()) == tokens["SwimmerNetwork"]["CRA"]
        ]
    )

    tusAmount = inferTusRewardsFromCraRewards(craAmount)

    return (tusAmount, craAmount)


def inferTusRewardsFromCraRewards(craAmount: Wei) -> Wei:
    """
    Given the CRA rewarded in a closeGame or settleGame transaction,
    return the corresponding TUS rewards
    """
    if craAmount == None:
        return None
    return Wei(craAmount * tusToCraRatio)
