"""
Use the "make" functions defined in this class to
dinamically instantiate strategies
"""

from src.strategies.loot.LootStrategy import LootStrategy
from src.strategies.loot.LowestBpLootStrategy import LowestBpLootStrategy
from src.strategies.reinforce.HighestBpReinforceStrategy import HighestBpReinforceStrategy
from src.strategies.reinforce.HighestMpReinforceStrategy import HighestMpReinforceStrategy
from src.strategies.reinforce.CheapestCrabReinforceStrategy import CheapestCrabReinforceStrategy
from src.strategies.reinforce.ReinforceStrategy import ReinforceStrategy

lootStrategies = {
    'LowestBp': LowestBpLootStrategy,
}

reinforceStrategies = {
    'CheapestCrab': CheapestCrabReinforceStrategy,
    'HighestBp': HighestBpReinforceStrategy,
    'HighestMp': HighestMpReinforceStrategy,
}

def makeLootStrategies(strategyName: str, *args, **kwargs) -> LootStrategy:
    strategyClass = lootStrategies.get(strategyName)
    if not strategyClass:
        return None
    return strategyClass(*args, **kwargs)

def makeReinforceStrategy(strategyName: str, *args, **kwargs) -> ReinforceStrategy:
    strategyClass = reinforceStrategies.get(strategyName)
    if not strategyClass:
        return None
    return strategyClass(*args, **kwargs)