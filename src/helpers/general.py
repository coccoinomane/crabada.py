from functools import reduce
from typing import Any, List
from collections import Counter
from random import uniform


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
    Return the n-th plus 1 element of a list or None if it is not set
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


def findInListOfDicts(l: List[dict[str, Any]], key: str, value: Any) -> Any:
    """
    Return the first dictionary in the list that has the
    given key value
    """
    return firstOrNone([item for item in l if item[key] == value])


def indexInList(l: List[Any], value: Any, doPop: bool = False) -> int:
    """
    Wrapper to the list.index(value) method which returns None
    if the value is not found, instead of raising an exception.
    """
    try:
        i = l.index(value)
        if doPop:
            l.pop(i)
        return i
    except ValueError:
        return None


def duplicatesInList(l: List[Any]) -> List[Any]:
    """
    Return duplicate elements in the given list

    Source: https://stackoverflow.com/a/9835819/2972183
    """
    return [item for item, count in Counter(l).items() if count > 1]


def flattenList(l: List[Any]) -> List[Any]:
    """
    Flatten a list

    Source: https://stackoverflow.com/a/46080186/2972183
    """
    return reduce(lambda x, y: x + y, l)


def randomize(x: float, d: float) -> float:
    """
    Return a number uniformly distributed between
    x*(1-d) and x*(1+d)
    """
    if d == 0:
        return x
    return x * (1 + uniform(-1, 1) * d)
