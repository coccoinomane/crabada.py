from typing import List
from random import randint


def getMiningClaims(n: int, winsPercent: int = 30) -> List[List[float]]:
    """
    Generate n claims of mining rewards
    """
    output = []

    for _ in range(0, n):
        if randint(1, 100) <= winsPercent:
            output.append([334.125, 4.125])
        else:
            output.append([136.6875, 1.6875])

    return output
