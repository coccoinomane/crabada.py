"""Configure the logging function.

For more advanced uses, see https://realpython.com/python-logging/"""

import logging
import logging.handlers
from src.common.dotenv import getenv

# Create a custom logger
logger = logging.getLogger(__name__)

# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.handlers.TimedRotatingFileHandler('storage/logs/app.log', 'midnight')
c_handler.setLevel(getenv('DEBUG_LEVEL', 'WARNING'))
f_handler.setLevel(getenv('DEBUG_LEVEL', 'WARNING'))

# Create formatters and add it to handlers
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)

logger.warning('This is a warning')
logger.error('This is an error')