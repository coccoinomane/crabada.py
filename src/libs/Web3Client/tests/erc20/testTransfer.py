from typing import cast
from eth_typing import Address
from src.common.config import nodeUri, users
from src.libs.Web3Client.AvalancheCErc20Web3Client import AvalancheCErc20Web3Client
from src.helpers.general import secondOrNone, thirdOrNone
from sys import argv
from pprint import pprint
from src.libs.Web3Client.helpers.debug import printTxInfo
from src.libs.Web3Client.exceptions import Web3ClientException
from web3.exceptions import ContractLogicError

# VARS
tokenAddress = cast(Address, secondOrNone(argv) or "")
to = cast(Address, thirdOrNone(argv) or "")

if not tokenAddress:
    print("Please provide a token address")
    exit(1)

if not to:
    print("Please provide a recipient")
    exit(1)

amount = 1

client = AvalancheCErc20Web3Client(
    nodeUri=nodeUri, privateKey=users[0]["privateKey"], contractAddress=tokenAddress
)

contractFunction = client.contract.functions.transfer(to, amount)

# TEST FUNCTIONS
def testBuild() -> None:
    pprint(client.buildContractTransaction(contractFunction))


def testSend() -> None:
    tx = client.buildContractTransaction(contractFunction)
    txHash = client.signAndSendTransaction(tx)
    printTxInfo(client, txHash)


# EXECUTE
try:
    testBuild()
except ContractLogicError as e:
    print(">>> CONTRACT EXCEPTION!")
    print(e)
except Web3ClientException as e:
    print(">>> CLIENT EXCEPTION!")
    print(e)

try:
    argv.index("--send")
    doSend = True
except ValueError:
    doSend = False

if doSend:
    try:
        testSend()
    except ContractLogicError as e:
        print(">>> CONTRACT EXCEPTION!")
        print(e)
    except Web3ClientException as e:
        print(">>> CLIENT EXCEPTION!")
        print(e)
