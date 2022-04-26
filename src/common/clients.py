"""Initialize crabada clients so that they can be used
by the scripts"""

from typing import cast
from eth_typing import Address
from src.common.config import nodeUri, users
from src.libs.CrabadaWeb3Client.CrabadaWeb3Client import CrabadaWeb3Client
from src.libs.CrabadaWeb2Client.CrabadaWeb2Client import CrabadaWeb2Client
from src.libs.Web3Client.Erc20Web3Client import Erc20Web3Client
from src.libs.Web3Client.Web3Client import Web3Client
from src.libs.Web3Client.Web3ClientFactory import makeErc20Client, makeWeb3Client


def makeCrabadaWeb2Client() -> CrabadaWeb2Client:
    """
    Return an initialized client to access Crabada's web endpoints
    """
    return CrabadaWeb2Client()


def makeCrabadaWeb3Client(
    upperLimitForBaseFeeInGwei: float = None,
) -> CrabadaWeb3Client:
    """
    Return an initialized client to interact with Crabada's
    smart contracts
    """
    return CrabadaWeb3Client(
        nodeUri=nodeUri,
        privateKey=users[0]["privateKey"],
        upperLimitForBaseFeeInGwei=upperLimitForBaseFeeInGwei,
    )


def makeAvalancheClient() -> Web3Client:
    """
    Return a generic client to interact with the Avalanche C Chain
    network
    """
    return makeWeb3Client(
        "Avalanche",
        nodeUri,
        privateKey=users[0]["privateKey"],
    )


def makeTusClient() -> Erc20Web3Client:
    """
    Return an initialized client to interact with the TUS
    token contract
    """
    tusContract = cast(Address, "0xf693248F96Fe03422FEa95aC0aFbBBc4a8FdD172")
    return makeErc20Client(
        "Avalanche",
        nodeUri,
        tusContract,
        privateKey=users[0]["privateKey"],
    )


def makeCraClient() -> Erc20Web3Client:
    """
    Return an initialized client to interact with the CRA
    token contract
    """
    craContract = cast(Address, "0xa32608e873f9ddef944b24798db69d80bbb4d1ed")
    return makeErc20Client(
        "Avalanche",
        nodeUri,
        craContract,
        privateKey=users[0]["privateKey"],
    )
