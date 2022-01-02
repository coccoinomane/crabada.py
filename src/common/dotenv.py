import os, dotenv
from typing import Any

# Load environment from .env
dotenv.load_dotenv()

# Shorthand to get environment variables
def getenv(key: str, default: Any = '') -> str:
    return os.getenv(key, default)