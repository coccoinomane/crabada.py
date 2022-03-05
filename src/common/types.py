from typing import Literal, NewType, TypedDict, List
from eth_typing import Address
from web3.types import Wei

Tus = NewType('Tus', int)

"""
Task assigned to a team
"""
TeamTask = Literal['loot', 'mine']

"""
Strategy that a team should follow to choose the best mine
to loot
"""
LootStrategyName = Literal['LowestBp']

"""
Strategy that the team should follow to get the best
reincorcement
"""
ReinforceStrategyName = Literal['CheapestCrab', 'HighestMp', 'HighestBp']

class ConfigTeam(TypedDict):
    id: int
    userAddress: Address
    battlePoints: int
    task: TeamTask
    lootStrategyName: LootStrategyName
    reinforceStrategyName: ReinforceStrategyName

class ConfigUser(TypedDict):
    address: Address
    privateKey: str
    maxPriceToReinforceInTus: Tus
    maxPriceToReinforceInTusWei: Wei
    teams: List[ConfigTeam]

class ConfigContract(TypedDict):
    address: Address
    abi: str