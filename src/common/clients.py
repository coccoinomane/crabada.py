"""Initialize crabada clients so that they can be used
by the scripts"""

from typing import cast
from src.common.config import nodeUri, users, contract, chainId
from src.libs.CrabadaWeb3Client.CrabadaWeb3Client import CrabadaWeb3Client
from src.libs.CrabadaWeb2Client.CrabadaWeb2Client import CrabadaWeb2Client

crabadaWeb2Client = CrabadaWeb2Client()

crabadaWeb3Client = cast(CrabadaWeb3Client,(CrabadaWeb3Client()
    .setNodeUri(nodeUri)
    .setContract(contract['address'], contract['abi'])
    .setCredentials(users[0]['address'], users[0]['privateKey'])
    .setChainId(chainId)))