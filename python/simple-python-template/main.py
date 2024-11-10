# config.py
import sys
from pathlib import Path

from dynaconf import Dynaconf
from loguru import logger

# Project structure setup
ROOT_DIR = Path(__file__).parent
LOGS_DIR = ROOT_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# Initialize settings
settings = Dynaconf(
    envvar_prefix="APP",
    root_path=Path(__file__).parent,
    load_dotenv=True,
    settings_files=["settings.toml", ".secrets.toml"],
    environments=True,
)

logger.remove()  # Remove the default handler

# Add console handler
logger.add(
    sys.stderr,  # Console output
    format="[<green>{time:YYYY-MM-DD HH:mm:ss}</green>] <level>{level: <8}</level> [{file}:{line}] {message}",
    level="DEBUG",
    colorize=True,
)

# Configure logging
logger.add(
    LOGS_DIR / "access.log",
    level="DEBUG",
    format="[{time:YYYY-MM-DD HH:mm:ss}] {level: <8} [{file}:{line}] {message}",
    rotation="1 MB",
    # retention="3 days",
)


if __name__ == "__main__":
    # Example usage
    logger.info("Application started")
    logger.debug("Debug message")
    logger.warning("Warning message")
    logger.error("Error message")

    # Example settings usage
    DEBUG = settings.get("DEBUG", False)
