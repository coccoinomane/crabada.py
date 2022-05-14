from pprint import pprint
from sys import argv
from typing import Tuple
from web3.types import TxReceipt, Wei
from src.helpers.donate import donate, getDonationAmounts, shouldDonate
from src.helpers.general import indexInList, secondOrNone, thirdOrNone
from src.common.clients import makeSwimmerNetworkClient
from src.helpers.rewards import getTusAndCraRewardsFromTxReceipt
from src.libs.Web3Client.Web3Client import Web3Client
from src.helpers.price import weiToCra, weiToTus
from src.libs.Web3Client.helpers.debug import pprintAttributeDict
from src.tests.donate import mocks
from src.common.config import donateFrequency, donatePercentage

# VARS
client = makeSwimmerNetworkClient()

doSend = indexInList(argv, "--send", doPop=True) is not None
n = int(secondOrNone(argv) or "0")  # create n fake claims
percentage = int(thirdOrNone(argv) or donatePercentage)

claims = mocks.getMiningClaims(n)
recentClaims = claims[-donateFrequency:]

# TEST FUNCTIONS
def testGetDonationAmounts() -> Tuple[Wei, Wei]:
    print(f">>> RECENT CLAIMS ({len(recentClaims)})")
    pprint(recentClaims)
    print(f">>> TOTAL CLAIMS")
    accumulator = [0, 0]
    for c in recentClaims:
        accumulator[0] += c[0]
        accumulator[1] += c[1]
    print(accumulator)
    print(">>> DONATION AMOUNTS IN WEI")
    tusAmount, craAmount = getDonationAmounts(recentClaims, percentage)
    print(tusAmount, craAmount)
    print(">>> DONATION AMOUNTS IN ETH")
    print(weiToTus(tusAmount), weiToCra(craAmount))
    print(">>> SHOULD DONATE?")
    print(shouldDonate(claims, donateFrequency))
    return (tusAmount, craAmount)


def testDonate() -> Tuple[TxReceipt, TxReceipt]:
    print(">>> DOING DONATION...")
    (tusReceipt, craReceipt) = donate(recentClaims, percentage)
    if not tusReceipt or not craReceipt:
        print(">>> ERROR: EMPTY RESULT")
        print("Maybe you have zero claims or set a percentage of 0?")
        exit(1)
    print(">>> TUS DONATED TX & GAS SPENT")
    pprintAttributeDict(tusReceipt)
    print(f"GAS SPENT IN ETH = {Web3Client.getGasSpentInEth(tusReceipt)}")
    print(">>> CRA DONATED TX & GAS SPENT")
    pprintAttributeDict(craReceipt)
    print(f"GAS SPENT IN ETH = {Web3Client.getGasSpentInEth(craReceipt)}")
    return (tusReceipt, craReceipt)


def testDonatedAmount(
    txReceiptTus: TxReceipt, txReceiptCra: TxReceipt
) -> Tuple[Wei, Wei]:
    (_, craDonated) = getTusAndCraRewardsFromTxReceipt(txReceiptCra)
    tusTx = client.getTransaction(tusReceipt["transactionHash"])
    tusDonated = tusTx["value"]
    print(">>> TUS DONATED")
    print(weiToTus(tusDonated))
    print(">>> CRA DONATED")
    print(weiToCra(craDonated))
    return (tusDonated, craDonated)


# EXECUTE
(tusToBeDonated, craToBeDonated) = testGetDonationAmounts()
if doSend:
    (tusReceipt, craReceipt) = testDonate()
    (tusDonated, craDonated) = testDonatedAmount(tusReceipt, craReceipt)
    assert tusToBeDonated == tusDonated
    assert craToBeDonated == craDonated
