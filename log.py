import sys
from loguru import logger

def LogToConsole(level: str, message: str):
    logger.add(sys.stderr, format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}", level="INFO")


def LogToFile(level: str, message: str):
    logger.add(sys.stderr, format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}", level="INFO")
    logger.add(
    "logs/app.log", 
    rotation="10 MB",     # Close current file and start a new one when it hits 500MB
    retention="10 days",   # Automatically delete log files older than 10 days
    compression="zip",     # Compress rotated log files into .zip format
    level="DEBUG"          # Capture everything from DEBUG level and above
)