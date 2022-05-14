import os, dotenv
from typing import Any, List
from src.common.exceptions import InvalidConfig, MissingConfig


dotenv.load_dotenv()


def getenv(key: str, default: Any = "") -> str:
    """
    Shorthand to get environment variables
    """
    return os.getenv(key, default)


def parseBool(key: str, default: bool = None) -> int:
    """
    Get an env variable and return False or True based on its value;
    return the default value if the variable is not found.

    Rules:
    - a string/number with the value of '1' will be cast to True
    - a string with the value 'true' or 'True' will be cast to True.
    - a string with the value 't' or 'T' will be cast to True.
    - anything else will be cast to False
    """
    value = getenv(key, None)
    if value is None:
        return default

    # Remove trailing comments and trim spaces
    value = value.split("#")[0].strip()

    # 'true', 'True' and '1' all mean True
    if value.lower() == "true" or value.lower() == "t" or value == "1":
        return True

    return False


def parseInt(key: str, default: int = None) -> int:
    """
    Get an env variable and cast it to integer; return the
    default value if the variable is not found; raises
    an error if the variable is not an integer.
    """
    value = getenv(key, None)
    if value is None:
        return default
    try:
        return int(value)
    except:
        raise InvalidConfig(f"Config value '{key}' must be an integer, {value} given")


def parseFloat(key: str, default: float = 0) -> float:
    """
    Get an env variable and cast it to a float; return the
    default value if the variable is not found; raises an
    error if the variable is not a float.
    """
    value = getenv(key, None)
    if value is None:
        return default
    try:
        return float(value)
    except:
        raise InvalidConfig(
            f"Config value '{key}' must be a float number, '{value}' given"
        )


def parsePercentage(key: str, default: float = 0) -> float:
    """
    Same as parseFloat, but raises an error if the value is smaller
    than 0 or larger than 100, and allows to use a trailing % sign
    """
    value = getenv(key, None)
    if value is None:
        return default

    # Allow to use a % trailing sign
    sanitizedValue = value.strip()
    if sanitizedValue[-1] == "%":
        sanitizedValue = sanitizedValue[:-1]

    # Cast to a number
    try:
        floatValue = float(sanitizedValue)
    except:
        raise InvalidConfig(
            f"Config value '{key}' must be a percentage, '{value}' given"
        )

    # Check that the % is within bounds
    if floatValue < 0:
        raise InvalidConfig(
            f"Config value '{key}' must be higher than or equal to 0%, '{value}' given"
        )
    if floatValue > 100:
        raise InvalidConfig(
            f"Config value '{key}' must be lower than 100%, '{value}' given"
        )

    return floatValue


def parseListOfStrings(key: str, default: List[str] = []) -> List[str]:
    """
    Parse a comma-separated string into a list of strings;
    return None if the variable is not found
    """
    value = getenv(key, None)
    if value is None:
        return default
    return [v.strip() for v in value.split(",")]


def parseListOfInts(key: str, default: List[int] = []) -> List[int]:
    """
    Parse a comma-separated string into a list of integers;
    return None if the variable is not found, raises an
    exception if the string elements are not castable to
    integers.
    """
    value = getenv(key, None)
    if value is None:
        return default
    return [int(v.strip()) for v in value.split(",")]
