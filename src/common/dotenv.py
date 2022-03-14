import os, dotenv
from typing import Any
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


def parseInt(key: str, default: int = 0) -> int:
    """
    Get an env variable and cast it to integer; return
    None if the variable is not found; raises an error
    if the variable is not an integer.
    """
    value = getenv(key, None)
    if value is not None:
        try:
            intValue = int(value)
        except:
            raise InvalidConfig(f"Config value {key} must be an integer, {value} given")
    return None if value is None else int(intValue)


def parseFloat(key: str, default: int = 0) -> int:
    """
    Get an env variable and cast it to a float; return
    None if the variable is not found; raises an error
    if the variable is not a float.
    """
    value = getenv(key, None)
    if value is not None:
        try:
            floatValue = float(value)
        except:
            raise InvalidConfig(
                f"Config value {key} must be a float number, {value} given"
            )
    return None if value is None else int(floatValue)
