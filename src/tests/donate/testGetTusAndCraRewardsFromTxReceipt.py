from sys import argv
from typing import cast
from src.helpers.general import secondOrNone
from src.common.clients import makeSwimmerNetworkClient
from src.helpers.rewards import getTusAndCraRewardsFromTxReceipt
from src.helpers.price import weiToCra, weiToTus
from eth_typing.encoding import HexStr

# VARS
txHash = cast(
    HexStr,
    (
        secondOrNone(argv)
        or "0x52c4490d11ad34f7d7203fcc7fcfad3f723365fad9012b518a57164bf9bb754a"
    ),
)
client = makeSwimmerNetworkClient()

# TEST FUNCTION
def test() -> None:
    txReceipt = client.getTransactionReceipt(txHash)
    (tusAmount, craAmount) = getTusAndCraRewardsFromTxReceipt(txReceipt)
    if craAmount == None:
        print(">>> NO REWARDS!")
    print(">>> TUS REWARD")
    print(weiToTus(tusAmount))
    print(">>> CRA REWARD")
    print(weiToCra(craAmount))


# EXECUTE
test()
