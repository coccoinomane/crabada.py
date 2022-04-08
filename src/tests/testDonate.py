from sys import argv
from typing import Tuple, cast
from web3.types import TxReceipt, Wei
from eth_typing import HexStr
from src.helpers.donate import donate, getDonationAmounts
from src.helpers.general import indexInList, secondOrNone, thirdOrNone
from src.common.clients import makeAvalancheClient
from src.helpers.rewards import getTusAndCraRewardsFromTxReceipt
from src.libs.Web3Client.Web3Client import Web3Client
from src.helpers.price import weiToCra, weiToTus
from src.libs.Web3Client.helpers.debug import pprintAttributeDict

# VARS
client = makeAvalancheClient()

doSend = indexInList(argv, "--send", doPop=True) is not None
percentage = int(secondOrNone(argv) or 1)
tx = cast(
    HexStr,
    (
        thirdOrNone(argv)
        or "0x143fbb963df559bacb1245a39ad586da80b68629906792e928787f467fa09ed8"
    ),
)
txReceipt = client.getTransactionReceipt(tx)

multiplier = 1

# TEST FUNCTIONS
def testGetRewards() -> None:
    (tusReward, craReward) = getTusAndCraRewardsFromTxReceipt(txReceipt)
    print(">>> TUS REWARD")
    print(weiToTus(tusReward))
    print(">>> CRA REWARD")
    print(weiToCra(craReward))


def testGetDonationAmounts() -> Tuple[Wei, Wei]:
    (tusToBeDonated, craToBeDonated) = getDonationAmounts(
        txReceipt, percentage, multiplier
    )
    print(">>> TUS TO BE DONATED")
    print(weiToTus(tusToBeDonated))
    print(">>> CRA TO BE DONATED")
    print(weiToCra(craToBeDonated))
    return (tusToBeDonated, craToBeDonated)


def testDonate() -> Tuple[TxReceipt, TxReceipt]:
    print(">>> DOING DONATION...")
    (tusReceipt, craReceipt) = donate(txReceipt, percentage, multiplier)
    if not tusReceipt or not craReceipt:
        print(">>> ERROR: EMPTY RESULT")
        print("Maybe you set a percentage of 0?")
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
    (tusDonated, _) = getTusAndCraRewardsFromTxReceipt(txReceiptTus)
    (_, craDonated) = getTusAndCraRewardsFromTxReceipt(txReceiptCra)
    print(">>> TUS DONATED")
    print(weiToTus(tusDonated))
    print(">>> CRA DONATED")
    print(weiToCra(craDonated))
    return (tusDonated, craDonated)


# EXECUTE
testGetRewards()
(tusToBeDonated, craToBeDonated) = testGetDonationAmounts()
if doSend:
    (tusReceipt, craReceipt) = testDonate()
    (tusDonated, craDonated) = testDonatedAmount(tusReceipt, craReceipt)
    assert tusToBeDonated == tusDonated
    assert craToBeDonated == craDonated
