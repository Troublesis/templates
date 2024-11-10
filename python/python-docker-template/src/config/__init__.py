"""
Configuration and logging setup module using Dynaconf and Loguru.
Provides centralized configuration management and structured logging capabilities.
"""

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from dynaconf import Dynaconf, Validator
from loguru import logger


class LogConfig:
    """Log format configurations and utility methods."""

    FORMATS = {
        "normal": "<green>{time:YYYY-MM-DD HH:mm:ss}</green> <level>{level: <8}</level> [{file}:{line}] {message}",
        "warning": "<yellow>{time:YYYY-MM-DD HH:mm:ss}</yellow> <level>{level: <8}</level> [{file}:{line}] {message}",
        "error": "<red>{time:YYYY-MM-DD HH:mm:ss}</red> <level>{level: <8}</level> [{file}:{line}] {message}",
    }

    @staticmethod
    def debug_filter(record: Dict[str, Any]) -> bool:
        """Filter out DEBUG level messages."""
        return record["level"].name != "DEBUG"


def setup_logger(debug_mode: bool = False, log_dir: Union[str, Path] = "logs") -> None:
    """
    Configure Loguru logger with multiple outputs and rotation policies.

    Args:
        debug_mode: Enable debug logging if True
        log_dir: Directory to store log files (can be string or Path object)
    """
    # Convert string to Path if necessary and create directory
    log_path = Path(log_dir)
    log_path.mkdir(exist_ok=True)

    # Remove default logger
    logger.remove()

    # Configure handlers
    logger.configure(
        handlers=[
            {
                "sink": sys.stderr,
                "format": LogConfig.FORMATS["normal"],
                "level": LOG_LEVEL if debug_mode else "INFO",
                "filter": None if debug_mode else LogConfig.debug_filter,
            },
            {
                "sink": log_path / "access.log",
                "format": LogConfig.FORMATS["normal"],
                "rotation": "100 MB",
                "retention": "7 days",
            },
            {
                "sink": log_path / "warning.log",
                "format": LogConfig.FORMATS["warning"],
                "level": "WARNING",
                "rotation": "100 MB",
            },
            {
                "sink": log_path / "error.log",
                "format": LogConfig.FORMATS["error"],
                "level": "ERROR",
                "rotation": "100 MB",
            },
        ]
    )


def create_settings(
    root_path: Union[str, Path] = Path(__file__).parent,
    settings_files: List[str] = ["settings.toml"],
    env_prefix: Optional[str] = None,
) -> Dynaconf:
    """
    Create and configure Dynaconf settings instance.

    Args:
        root_path: Base path for configuration files (can be string or Path object)
        settings_files: List of configuration files to load
        env_prefix: Prefix for environment variables

    Returns:
        Configured Dynaconf instance
    """
    return Dynaconf(
        envvar_prefix=False,
        load_dotenv=True,
        root_path=root_path,
        settings_files=settings_files,
        environments=True,
        validators=[
            Validator("DEBUG", must_exist=True, is_type_of=bool),
            Validator(
                "LOG_LEVEL",
                # must_exist=True,
                is_in=["DEBUG", "INFO", "WARNING", "ERROR"],
            ),
        ],
    )


# Initialize settings and logger
settings = create_settings()
LOG_LEVEL = settings.get("LOG_LEVEL", "INFO")
setup_logger(debug_mode=settings.get("DEBUG", False), log_dir=Path("logs"))


"""
Usage Examples:

1. Basic Logging:
    logger.info("Application started")
    logger.debug("Debug information")
    logger.warning("Warning message")
    logger.error("Error occurred")
    logger.critical("Critical failure")

2. Accessing Configuration Values:
    # Get simple values with defaults
    debug_mode = settings.get("DEBUG", False)
    log_level = settings.get("LOG_LEVEL", "INFO")

    # Environment-specific settings
    prod_db = settings.from_env("production").database
    dev_settings = settings.from_env("development")

    # Type conversion
    is_enabled = settings.as_bool("FEATURE_FLAG")
    config_dict = settings.as_json("CONFIG_JSON")

    # Nested settings with defaults
    db_user = settings.database.credentials.get("username", "default_user")

3. Custom Logger Instance:
    custom_logger = logger.bind(context="my_module")
    custom_logger.info("Module-specific log")

4. Temporary Log File:
    tmp_log_path = Path("temp") / "process.log"
    with logger.add(tmp_log_path, rotation="1 day") as log_id:
        logger.info("Temporary process started")
        # ... process logic ...
        logger.info("Temporary process completed")

5. Environment Variables:
    # Export variables:
    # export DYNACONF_API_KEY="secret-key"
    # export DYNACONF_DEBUG="true"
    # export DYNACONF_LOG_LEVEL="INFO"

    # Access in code:
    api_key = settings.get("API_KEY")
    log_level = settings.get("LOG_LEVEL")
"""

if __name__ == "__main__":
    # Example usage
    logger.info("Application initialized")
    logger.debug("Configuration loaded")
    logger.warning("System resources running low")
    logger.error("Failed to connect to database")
    logger.critical("System shutdown initiated")
