from src.helpers.general import duplicatesInList
from src.helpers.general import flattenList

# VARS


# TEST FUNCTIONS
def test() -> None:
    assert duplicatesInList([1, 2, 3, 2, 3, 4, 3, 4, 5]) == [2, 3, 4]
    assert flattenList([[1, 2, 3], [2, 3, 4], [3, 4, 5]]) == [1, 2, 3, 2, 3, 4, 3, 4, 5]


# EXECUTE
test()
