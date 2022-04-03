import os, dotenv
from typing import Any, List
from src.common.exceptions import InvalidConfig, MissingConfig

# Load environment from .env
if not os.path.isfile(".env"):
    raise MissingConfig(".env file not found")
dotenv.load_dotenv()


def getenv(key: str, default: Any = "") -> str:
    """
    Shorthand to get environment variables
    """
    return os.getenv(key, default)


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
        raise InvalidConfig(f"Config value {key} must be an integer, {value} given")


def parseFloat(key: str, default: int = 0) -> float:
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
        raise InvalidConfig(f"Config value {key} must be a float number, {value} given")


def parseListOfStrings(key: str, default: List[str] = []) -> List[str]:
    """
    Parse a comma-separated string into a list of strings;
    return None if the variable is not found
    """
    value = getenv(key, None)
    if value is None:
        return default
    return [v.strip() for v in value.split(",")]
