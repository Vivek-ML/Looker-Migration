import logging
import os
import time

# Create logs directory if not exists
log_dir = os.path.join(os.path.dirname(__file__), "../logs")
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

LOG_FILE = os.path.join(log_dir, "selenium_log.log")

# Configure logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8"
)

def log_message(message, level="INFO"):
    """Log messages with structured format."""
    if level == "INFO":
        logging.info(message)
    elif level == "ERROR":
        logging.error(message)
    elif level == "WARNING":
        logging.warning(message)
    print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} | {level} | {message}")
