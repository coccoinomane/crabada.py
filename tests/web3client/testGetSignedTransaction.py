import sys
sys.path.insert(1, '../..')
from common.config import nodeUri, contract, users, chainId
from libs.crabada.web3client.Web3Client import Web3Client
from pprint import pprint

# VARS
client = (Web3Client()
    .setContractAddress(contract['address'])
    .setNodeUri(nodeUri)
    .setAbi(contract['abi'])
    .setCredentials(users[0]['address'], users[0]['privateKey'])
    .setChainId(chainId)
    .init())

to = "0xBc3a38C981B13625FAF7729fF105Cb6E15bdDE3A"
valueInEth = 0.00001 # ETH / AVAX / etc
gas = 200000 # units
gasPrice = 50 # gwei

# TEST FUNCTIONS
def testGetSignedTransaction():
    tx = client.buildSignedTransaction(to, valueInEth, gas, gasPrice)
    print(">>> SIGNED TX")
    pprint(tx)

def sendSignedTransaction():
    tx = client.buildSignedTransaction(to, valueInEth, gas, gasPrice)
    txHash = client.sendSignedTransaction(tx)
    print(">>> TX SENT!")
    print(txHash)

# EXECUTE
testGetSignedTransaction()
if (len(sys.argv) > 1 and sys.argv[1] == '--send'):
    sendSignedTransaction()