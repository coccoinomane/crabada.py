from web3 import Web3
from pprint import pprint

# VARS
# Convert one of 'currency' into wei.
# From docs: Must be one of wei/kwei/babbage/femtoether/mwei/lovelace/picoether/gwei/shannon/nanoether/nano/szabo/microether/micro/finney/milliether/milli/ether/kether/grand/mether/gether/tether
currency = 'ether'

# TEST FUNCTIONS
def testToWei():
    pprint(Web3.toWei(1, currency))

# EXECUTE
testToWei()