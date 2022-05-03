"""Create a logger for app-related events (bugs, info, etc)

For more advanced uses, see https://realpython.com/python-logging/"""

import os
import logging
import logging.handlers
from .dotenv import getenv

# Create a custom logger
logger = logging.getLogger(__name__)
logger.setLevel(getenv("DEBUG_LEVEL", "WARNING"))

logFilepath = os.path.join(getenv("STORAGE_FOLDER", "storage"), "logs/app", "app.log")
os.makedirs(os.path.dirname(logFilepath), exist_ok=True)

# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.handlers.TimedRotatingFileHandler(logFilepath, "midnight")

c_handler.setLevel(getenv("DEBUG_LEVEL", "WARNING"))
f_handler.setLevel(getenv("DEBUG_LEVEL", "WARNING"))

# Create formatters and add it to handlers
c_format = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
f_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)
