from sys import argv
from src.helpers.donate import (
    getDonationAmounts,
    shouldDonate,
)
from src.helpers.general import secondOrNone
from src.common.config import donatePercentage, donateFrequency
from pprint import pprint
from src.helpers.price import weiToCra, weiToTus
from src.tests.donate import mocks

# VARS
n = int(secondOrNone(argv) or "0")  # create n fake claims
claims = mocks.getMiningClaims(n)
recentClaims = claims[-donateFrequency:]

# TEST FUNCTION
def test() -> None:
    print(f">>> RECENT CLAIMS ({len(recentClaims)})")
    pprint(recentClaims)
    print(f">>> TOTAL CLAIMS")
    accumulator = [0, 0]
    for c in recentClaims:
        accumulator[0] += c[0]
        accumulator[1] += c[1]
    print(accumulator)
    print(">>> DONATION AMOUNTS IN WEI")
    tusAmount, craAmount = getDonationAmounts(recentClaims, donatePercentage)
    print(tusAmount, craAmount)
    if craAmount:
        print(">>> DONATION AMOUNTS IN ETH")
        print(weiToTus(tusAmount), weiToCra(craAmount))
    print(">>> SHOULD DONATE?")
    print(shouldDonate(claims, donateFrequency))


# EXECUTE
test()
