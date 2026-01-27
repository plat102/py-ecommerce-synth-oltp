import logging
import sys
import os
from pathlib import Path
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(BASE_DIR / ".env", override=True)
env_log_dir = os.getenv("LOG_DIR", "logs")
LOG_DIR_PATH = (BASE_DIR / env_log_dir).resolve()

def setup_logging(log_level=logging.DEBUG, log_dir=LOG_DIR_PATH):
    """3 handlers
    - Console
    - App
    - Error
    """
    # Ensure log dir
    os.makedirs(log_dir, exist_ok=True)
    log_file_app = os.path.join(log_dir, "app.log")
    log_file_error = os.path.join(log_dir, "error.log")

    # Common format
    console_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
    file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Setup root & Clean up handlers (avoid double log)
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    # ----- Handlers -----
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_format)
    root_logger.addHandler(console_handler)

    # General handler (rotate files)
    # File 10 MB, keep 10 backup
    app_handler = RotatingFileHandler(
        log_file_app, maxBytes=10*1024*1024, backupCount=5, encoding='utf-8'
    )
    app_handler.setLevel(logging.DEBUG)
    app_handler.setFormatter(file_format)
    root_logger.addHandler(app_handler)

    # Error handler
    error_handler = RotatingFileHandler(
        log_file_error, maxBytes=10*1024*1024, backupCount=5, encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(file_format)
    root_logger.addHandler(error_handler)

    logging.info(f'Logging initialized. Logs directory: {os.path.abspath(log_dir)}"')
    return logging.getLogger('mock_ecommerce')

# Create default logger for importing from other modules
logger = setup_logging()
