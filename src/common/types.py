from typing import Literal, NewType, TypedDict, List
from eth_typing import Address
from web3.types import Wei

Tus = NewType('Tus', int)

Task = Literal['loot', 'mine']
LootStrategy = Literal['LowestBp']
ReinforceStrategy = Literal['CheapestCrab', 'HighestMp', 'HighestBp']

class ConfigTeam(TypedDict):
    id: int
    userAddress: Address
    task: Task
    lootStrategy: LootStrategy
    reinforceStrategy: ReinforceStrategy
class ConfigUser(TypedDict):
    name: str
    address: Address
    privateKey: str
    maxPriceToReinforceInTus: Tus
    maxPriceToReinforceInTusWei: Wei
    teams: List[ConfigTeam]

class ConfigContract(TypedDict):
    address: Address
    abi: str