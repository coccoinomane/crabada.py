from web3 import Web3

myEthAddress = '0x335A9431374bF1A5Ae05Ac2051a7B1a6e0b26D67'
infuraProjectId = '7aeef75cf44f442ca5dff936c84b3f69'

w3 = Web3(Web3.HTTPProvider(f'https://mainnet.infura.io/v3/{infuraProjectId}'))

# Get information about the latest block
# print(w3.eth.getBlock('latest'))

# Get the ETH balance of an address 
print(f'ETH BALANCE = {w3.eth.getBalance(myEthAddress)/1000000000000000000}')