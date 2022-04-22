from src.common.txLogger import logTx
from src.libs.PangolinRouterWeb3Client.PangolinRouterWeb3Client import (
    PangolinRouterWeb3Client,
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


def swapTusToAvax(user: User, tus: float) -> int:
    """
    tus here is in wei
    """
    client = PangolinRouterWeb3Client(
        nodeUri=nodeUri,
        privateKey=users[0]["privateKey"],
        upperLimitForBaseFeeInGwei=user.config["mineMaxGasInGwei"],
    )
    amtsOut = client.getAmountsOut(tus, TUS_TO_AVAX_PATH)
    amtOut = amtsOut[len(amtsOut) - 1]
    # account for slippage
    amtOutMin = int(amtOut / 100 * 99.5)
    txHash = client.swapExactTokensForAvax(tus, amtOutMin, TUS_TO_AVAX_PATH)
    txLogger.info(txHash)
    txReceipt = client.getTransactionReceipt(txHash)
    logTx(txReceipt)
    return 1
