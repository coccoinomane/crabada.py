from sys import argv
from src.helpers.donate import shouldDonate
from src.helpers.general import secondOrNone
from src.common.config import donateFrequency, donatePercentage

# VARS
n = int(secondOrNone(argv) or "1000")

# TEST FUNCTION
def test() -> None:
    nDonations = 0
    for i in range(0, n):
        if shouldDonate():
            nDonations += 1
    print(f">>> DONATIONS IN {n} TRANSACTIONS")
    print(nDonations)
    print(f">>> EXPECTED")
    if donatePercentage is not None and donatePercentage > 0:
        print(float(n) / donateFrequency)
    else:
        print(0)


# EXECUTE
test()
