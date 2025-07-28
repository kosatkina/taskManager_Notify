import logging
import os

LOG_DIR = "logs"
LOG_FILE_PATH = "logs/notify.log"

# Create directory and log file if does not exist
os.makedirs(LOG_DIR, exist_ok=True)

# Create and configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create file handler to write logs to a file
file_handler = logging.FileHandler(LOG_FILE_PATH, encoding='utf-8')
file_handler.setLevel(logging.INFO)

# Define log message format and add formatter to the file handler
log_format = "%(asctime)s - %(levelname)s - %(message)s"
formatter = logging.Formatter(log_format)
file_handler.setFormatter(formatter)

# Add file handler to the logger
if not logger.hasHandlers():
    logger.addHandler(file_handler)
