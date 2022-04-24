from typing import Literal, NewType, Tuple, TypedDict, List
from eth_typing import Address
from web3.types import Wei

Tus = NewType("Tus", float)
Cra = NewType("Cra", float)

"""
Task assigned to a team
"""
TeamTask = Literal["loot", "mine"]


class ConfigTeam(TypedDict):
    id: int  # team id in Crabada
    userAddress: Address
    battlePoints: int
    task: TeamTask
    lootStrategies: List[str]
    reinforceStrategies: List[str]
    reinforcementToPick: int
    teamNumber: int  # internal team number (if in group, relative to group)
    groupNumber: int  # internal group number (0 if team not in a group)


class ConfigUser(TypedDict):
    address: Address
    privateKey: str
    reinforcementMaxPriceInTus: Tus
    reinforcementMaxPriceInTusWei: Wei
    reinforcementMaxGasInGwei: float
    mineMaxGasInGwei: float
    closeMineMaxGasInGwei: float
    closeLootMaxGasInGwei: float
    teams: List[ConfigTeam]


class ConfigContract(TypedDict):
    address: Address
    abi: str
