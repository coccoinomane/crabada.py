from typing import Literal, NewType, TypedDict, List
from eth_typing import Address
from web3.types import Wei

Tus = NewType("Tus", float)

"""
Task assigned to a team
"""
TeamTask = Literal["loot", "mine"]


class ConfigTeam(TypedDict):
    id: int
    userAddress: Address
    battlePoints: int
    task: TeamTask
    lootStrategyName: str
    reinforceStrategyName: str


class ConfigUser(TypedDict):
    address: Address
    privateKey: str
    reinforcementMaxPriceInTus: Tus
    reinforcementMaxPriceInTusWei: Wei
    reinforcementToPick: int
    teams: List[ConfigTeam]


class ConfigContract(TypedDict):
    address: Address
    abi: str
