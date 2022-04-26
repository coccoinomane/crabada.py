from sys import argv
from src.helpers.donate import (
    deleteClaimsLog,
    getClaimsFromLog,
    logClaim,
    shouldDonate,
)
from src.helpers.general import secondOrNone
from src.common.config import donateFrequency
from src.tests.donate import mocks

# VARS
n = int(secondOrNone(argv) or "0")  # create n fake claims
claims = mocks.getMiningClaims(n)

# TEST FUNCTION
def test() -> None:
    print(shouldDonate(claims, donateFrequency))


# EXECUTE
try:
    test()
finally:
    if n:
        deleteClaimsLog()
