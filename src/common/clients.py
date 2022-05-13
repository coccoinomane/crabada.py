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


def makeSwimmerNetworkClient() -> Web3Client:
    """
    Return a generic client to interact with the Swimmer Network
    Avalanche subnet
    """
    return makeWeb3Client(
        "SwimmerNetwork",
        nodeUri,
        privateKey=users[0]["privateKey"],
    )


def makeAvalancheTusClient() -> Erc20Web3Client:
    """
    Return an initialized client to interact with the TUS
    token contract on the Avalanche C-Chain
    """
    tusContract = cast(Address, "0xf693248F96Fe03422FEa95aC0aFbBBc4a8FdD172")
    return makeErc20Client(
        "Avalanche",
        nodeUri,
        tusContract,
        privateKey=users[0]["privateKey"],
    )


def makeAvalancheCraClient() -> Erc20Web3Client:
    """
    Return an initialized client to interact with the CRA
    token contract on the Avalanche C-Chain
    """
    craContract = cast(Address, "0xa32608e873f9ddef944b24798db69d80bbb4d1ed")
    return makeErc20Client(
        "Avalanche",
        nodeUri,
        craContract,
        privateKey=users[0]["privateKey"],
    )


def makeSwimmerWtusClient() -> Erc20Web3Client:
    """
    Return an initialized client to interact with the WTUS
    token contract on the Swimmer Network Avalanche subnet.

    On Swimmer, WTUS is the wrapped version of TUS. Please note
    that to send 'regular' TUS, you just need to use the sendEth
    method in Web3Client.
    """
    wtusContract = cast(Address, "0x9c765eEE6Eff9CF1337A1846c0D93370785F6C92")
    return makeErc20Client(
        "SwimmerNetwork",
        nodeUri,
        wtusContract,
        privateKey=users[0]["privateKey"],
    )


def makeSwimmerCraClient() -> Erc20Web3Client:
    """
    Return an initialized client to interact with the CRA
    token contract on the Swimmer Network Avalanche subnet
    """
    craContract = cast(Address, "0xC1a1F40D558a3E82C3981189f61EF21e17d6EB48")
    return makeErc20Client(
        "SwimmerNetwork",
        nodeUri,
        craContract,
        privateKey=users[0]["privateKey"],
    )
