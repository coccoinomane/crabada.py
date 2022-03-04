import os, dotenv
from typing import Any
from src.common.exceptions import MissingConfig

# Load environment from .env
if (not os.path.isfile('.env')):
    raise MissingConfig(".env file not found")
dotenv.load_dotenv()

# Shorthand to get environment variables
def getenv(key: str, default: Any = '') -> str:
    return os.getenv(key, default)