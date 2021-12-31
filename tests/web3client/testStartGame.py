import sys
sys.path.insert(1, '../..')
from common.config import nodeUri, users, contract, chainId
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

# Gas
to = "0xBc3a38C981B13625FAF7729fF105Cb6E15bdDE3A"
valueInEth = 0.00001 # ETH / AVAX / etc
gas = 200000 # units
gasPrice = 50 # gwei

# Contract
contractFunction = client.contract.functions.startGame

# TEST FUNCTIONS
def testGetContract():
    userAddress = teams[0].userAddress
    userKey = [u for u in users if u.address == userAddress]
    
    output = client.startGame(usersteams[0].id)
    
    pprint(vars(client.getContract()))
    pprint(vars(client.getContract()))
    print(">>> CONTRACT FUNCTIONS")
    pprint(vars(client.getContract().functions))

# EXECUTE
testGetContract()