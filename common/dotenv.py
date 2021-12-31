import os, dotenv

# Load environment from .env
dotenv.load_dotenv()

# Shorthand to get environment variables
def getenv(key: str):
    return os.environ.get(key)