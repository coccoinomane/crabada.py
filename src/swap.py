from eth_typing import ChecksumAddress
from src.common.txLogger import logTx
from src.libs.RouterWeb3Client.PangolinRouterWeb3Client import (
    PangolinRouterWeb3Client,
)
from src.libs.RouterWeb3Client.TraderJoeRouterWeb3Client import (
    TraderJoeRouterWeb3Client,
)
from src.models.User import User
from src.common.config import nodeUri, users
from src.common.constants import tokens
from web3 import Web3
from src.common.txLogger import txLogger

TUS_TO_AVAX_PATH = [
    Web3.toChecksumAddress("0xf693248f96fe03422fea95ac0afbbbc4a8fdd172"),
    Web3.toChecksumAddress("0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7"),
]

CRA_TO_AVAX_PATH = [
    Web3.toChecksumAddress("0xA32608e873F9DdEF944B24798db69d80Bbb4d1ed"),
    Web3.toChecksumAddress("0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7"),
]


def swapTokenToAvaxPangolin(
    user: User, amtIn: float, path: list[ChecksumAddress]
) -> None:
    """
    amtIn here is in wei
    """
    client = PangolinRouterWeb3Client(
        nodeUri=nodeUri,
        privateKey=users[0]["privateKey"],
        upperLimitForBaseFeeInGwei=user.config["mineMaxGasInGwei"],
    )
    amtsOut = client.getAmountsOut(amtIn, path)
    amtOut = amtsOut[len(amtsOut) - 1]
    # account for slippage
    amtOutMin = int(amtOut / 100 * 99.5)
    txHash = client.swapExactTokensForAvax(amtIn, amtOutMin, path)
    txLogger.info(txHash)
    txReceipt = client.getTransactionReceipt(txHash)
    logTx(txReceipt)


def swapTokenToAvaxTraderJoe(
    user: User, amtIn: float, path: list[ChecksumAddress]
) -> None:
    """
    amtIn here is in wei
    """
    client = TraderJoeRouterWeb3Client(
        nodeUri=nodeUri,
        privateKey=users[0]["privateKey"],
        upperLimitForBaseFeeInGwei=user.config["mineMaxGasInGwei"],
    )
    amtsOut = client.getAmountsOut(amtIn, path)
    amtOut = amtsOut[len(amtsOut) - 1]
    # account for slippage
    amtOutMin = int(amtOut / 100 * 99.5)
    txHash = client.swapExactTokensForAvax(amtIn, amtOutMin, path)
    txLogger.info(txHash)
    txReceipt = client.getTransactionReceipt(txHash)
    logTx(txReceipt)
