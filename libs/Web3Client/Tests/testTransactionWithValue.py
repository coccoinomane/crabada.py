from sys import argv
from common.config import nodeUri, users, chainId
from libs.Web3Client.AvalancheWeb3Client import AvalancheWeb3Client
from libs.Web3Client.Tests.helpers import printTxInfo
from pprint import pprint

# VARS
client = (AvalancheWeb3Client()
    .setNodeUri(nodeUri)
    .setCredentials(users[0]['address'], users[0]['privateKey'])
    .setChainId(chainId)
    .setMaxPriorityFeePerGasInGwei(2))

to = "0xBc3a38C981B13625FAF7729fF105Cb6E15bdDE3A"
valueInEth = 0.00001 # ETH / AVAX / etc

# TEST FUNCTIONS
def testBuildTransactionWithValue():
    tx = client.buildTransactionWithValue(to, valueInEth)
    print(">>> TX")
    pprint(tx)

def testSignTransaction():
    tx = client.buildTransactionWithValue(to, valueInEth)
    signedTx = client.signTransaction(tx)
    print(">>> SIGNED TX")
    pprint(signedTx)

def testSendSignedTransaction():
    tx = client.buildTransactionWithValue(to, valueInEth)
    signedTx = client.signTransaction(tx)
    txHash = client.sendSignedTransaction(signedTx)
    printTxInfo(client, txHash)

# EXECUTE
testBuildTransactionWithValue()
testSignTransaction()
if (len(argv) > 1 and argv[1] == '--send'):
    testSendSignedTransaction()