from pprint import pprint
from sys import argv
from typing import Tuple, cast
from web3.types import TxReceipt, Wei
from src.helpers.general import secondOrNone
from src.common.clients import makeSwimmerNetworkClient
from src.helpers.rewards import getTusAndCraRewardsFromTxReceipt
from src.libs.Web3Client.Web3Client import Web3Client
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
    (tusDonated, craDonated) = getTusAndCraRewardsFromTxReceipt(txReceipt)
    print(">>> TUS DONATED")
    print(weiToTus(tusDonated))
    print(">>> CRA DONATED")
    print(weiToCra(craDonated))


# EXECUTE
test()
