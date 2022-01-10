from typing import Any, List

def firstOrNone(list: List[Any]) -> Any:
    """Return the first element of a list or None
    if 1) it is not set or 2) it is falsey"""
    try:
        return list[0]
    except:
        return None
    
def secondOrNone(list: List[Any]) -> Any:
    """Return the second element of a list or None
    if 1) it is not set or 2) it is falsey"""
    try:
        return list[1]
    except:
        return None

def thirdOrNone(list: List[Any]) -> Any:
    """Return the third element of a list or None
    if 1) it is not set or 2) it is falsey"""
    try:
        return list[2]
    except:
        return None

def findInList(l: List[dict[str, Any]], key: str, value: Any) -> Any:
    """
    Search a list of dictionaries for a specific one
    """
    return firstOrNone([item for item in l if item[key] == value])