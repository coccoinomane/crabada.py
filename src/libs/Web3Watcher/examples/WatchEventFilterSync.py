# type: ignore

"""
How to watch smart contract events using web3.eth.filter,
synchronously.

Here we use the StartGame event of the Crabada game contract on
Avalanche, so make sure to set the env variable WEB3_PROVIDER_URI
to an Avalanche Web Socket.

Crabada Contract: https://snowtrace.io/tx/0x41705baf18b1ebc8ec204926a8524d3530aada11bd3c249ca4a330ed047f005e

Taken from https://web3py.readthedocs.io/en/stable/filters.html?highlight=contract%20watch#examples-listening-for-events
"""

import logging
from web3.auto import w3
import time

CRABADA_CONTRACT = "0x82a85407BD612f52577909F4A58bfC6873f14DA8"
CRABADA_ABI = '[{"inputs":[{"internalType":"uint256","name":"teamId","type":"uint256"},{"internalType":"uint256","name":"position","type":"uint256"},{"internalType":"uint256","name":"crabadaId","type":"uint256"}],"name":"addCrabadaToTeam","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"gameId","type":"uint256"},{"internalType":"uint256","name":"attackTeamId","type":"uint256"}],"name":"attack","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"gameId","type":"uint256"}],"name":"closeGame","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"crabadaId1","type":"uint256"},{"internalType":"uint256","name":"crabadaId2","type":"uint256"},{"internalType":"uint256","name":"crabadaId3","type":"uint256"}],"name":"createTeam","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256[]","name":"crabadaIds","type":"uint256[]"}],"name":"deposit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"gameId","type":"uint256"},{"internalType":"uint256","name":"crabadaId","type":"uint256"},{"internalType":"uint256","name":"borrowPrice","type":"uint256"}],"name":"reinforceAttack","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"gameId","type":"uint256"},{"internalType":"uint256","name":"crabadaId","type":"uint256"},{"internalType":"uint256","name":"borrowPrice","type":"uint256"}],"name":"reinforceDefense","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"teamId","type":"uint256"},{"internalType":"uint256","name":"position","type":"uint256"}],"name":"removeCrabadaFromTeam","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"crabadaId","type":"uint256"},{"internalType":"uint256","name":"price","type":"uint256"}],"name":"setLendingPrice","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"gameId","type":"uint256"}],"name":"settleGame","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"teamId","type":"uint256"}],"name":"startGame","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256[]","name":"crabadaIds","type":"uint256[]"}],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"gameId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"teamId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"gameDuration","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"craReward","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"tusReward","type":"uint256"}],"name":"StartGame","type":"event"}]'

logger = logging.getLogger(__name__)


def handle_event(event):
    logger.warning("A new event was emitted!")
    print(event)
    # and whatever


def log_loop(event_filter, poll_interval):
    while True:
        newEvents = event_filter.get_new_entries()
        if not newEvents:
            logger.warning("No new event emitted")
        for event in newEvents:
            handle_event(event)
        time.sleep(poll_interval)


def main():
    contract = w3.eth.contract(
        address=CRABADA_CONTRACT,
        abi=CRABADA_ABI,
    )
    eventFilter = contract.events.StartGame().createFilter(fromBlock="latest")
    log_loop(eventFilter, 2)


if __name__ == "__main__":
    main()
