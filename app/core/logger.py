import sys
import os
from loguru import logger
from datetime import datetime

# Remove default handler
logger.remove()

# Create logs directory if it doesn't exist
log_dir = os.path.join(os.path.dirname(__file__), "../../logs")
os.makedirs(log_dir, exist_ok=True)

# Log level based on environment
log_level = os.getenv("LOG_LEVEL", "INFO")

# Console handler - for development/debugging
logger.add(
    sys.stdout,
    level=log_level,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    colorize=True,
)

# File handler - for all logs
logger.add(
    os.path.join(log_dir, "app.log"),
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    rotation="500 MB",
    retention="10 days",
    compression="zip",
)

# File handler - for errors only
logger.add(
    os.path.join(log_dir, "error.log"),
    level="ERROR",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    rotation="500 MB",
    retention="30 days",
)
