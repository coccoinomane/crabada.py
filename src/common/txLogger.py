"""Create a separate logger to exclusively track transaction
sent to the blockchain.

This logger will print the tx to a transactions.log file
in addition to the standard handlers specified in logger.py"""

import logging
import logging.handlers

from eth_typing.encoding import HexStr
from web3.main import Web3
from web3.types import TxReceipt
from src.common.logger import f_handler, c_handler

# Create a custom logger
txLogger = logging.getLogger(__name__)
txLogger.setLevel("DEBUG")

# Create handlers
tx_handler = logging.handlers.TimedRotatingFileHandler(
    "storage/logs/transactions/transactions.log", "midnight"
)
tx_handler.setLevel("DEBUG")

# Create formatters and add it to handlers
tx_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
tx_handler.setFormatter(tx_format)

# Add handlers to the logger
txLogger.addHandler(tx_handler)
txLogger.addHandler(f_handler)
txLogger.addHandler(c_handler)


def logTx(txReceipt: TxReceipt) -> None:
    """Given a tx receipt, print to screen the transaction details
    and its cost"""
    txLogger.debug(txReceipt)
    ethSpent = Web3.fromWei(
        txReceipt["effectiveGasPrice"] * txReceipt["gasUsed"], "ether"
    )
    txLogger.debug("Spent " + str(ethSpent) + " ETH")
