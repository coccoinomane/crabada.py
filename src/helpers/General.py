from typing import Any, List

def firstOrNone(list: List[Any]) -> Any:
    """Return the first element of a list or None
    if 1) it is not set or 2) it is falsey"""
    try:
        return list[0]
    except:
        return None