from typing import Any, List


def firstOrNone(list: List[Any]) -> Any:
    """
    Return the first element of a list or None if it is not set
    """
    return nthOrNone(list, 0)


def secondOrNone(list: List[Any]) -> Any:
    """
    Return the second element of a list or None if it is not set
    """
    return nthOrNone(list, 1)


def thirdOrNone(list: List[Any]) -> Any:
    """
    Return the third element of a list or None if it is not set
    """
    return nthOrNone(list, 2)


def fourthOrNone(list: List[Any]) -> Any:
    """
    Return the fourth element of a list or None if it is not set
    """
    return nthOrNone(list, 3)


def nthOrNone(list: List[Any], n: int) -> Any:
    """
    Return the n-th element of a list or None if it is not set
    """
    try:
        return list[n]
    except:
        return None


def nthOrLastOrNone(list: List[Any], n: int) -> Any:
    """
    Return the n-th element of a list; if it is not set, return
    the last element of the list; if it is not set, return none.
    """
    if not list:
        return None
    return list[n] if len(list) > n else list[-1]


def findInList(l: List[dict[str, Any]], key: str, value: Any) -> Any:
    """
    Search a list of dictionaries for a specific one
    """
    return firstOrNone([item for item in l if item[key] == value])
