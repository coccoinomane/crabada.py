"""Initialize crabada clients so that they can be used
by the scripts"""

from typing import cast
from src.common.config import nodeUri, users
from src.libs.CrabadaWeb3Client.CrabadaWeb3Client import CrabadaWeb3Client
from src.libs.CrabadaWeb2Client.CrabadaWeb2Client import CrabadaWeb2Client


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
