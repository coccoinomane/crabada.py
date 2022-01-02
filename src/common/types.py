from typing import TypedDict, List
from eth_typing import Address

class ConfigTeam(TypedDict):
    id: int
    userAddress: Address

class ConfigUser(TypedDict):
    name: str
    address: Address
    privateKey: str
    teams: List[ConfigTeam]

class ConfigContract(TypedDict):
    address: Address
    abi: str
