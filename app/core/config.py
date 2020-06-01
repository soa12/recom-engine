import logging
import sys
from starlette.config import Config
from starlette.datastructures import Secret
from starlette.datastructures import CommaSeparatedStrings
from typing import List
from loguru import logger
from app.core.logging import InterceptHandler

APP_VERSION = "0.0.1"
APP_NAME = "Recommendation Engine"
API_PREFIX = "/api"

config = Config(".env")

API_KEY: Secret = config("API_KEY", cast=Secret)
IS_DEBUG: bool = config("IS_DEBUG", cast=bool, default=False)
CF_NEAREST_NEIGHBORS = config("CF_NEAREST_NEIGHBORS", cast=int, default=10)

# DEFAULT_MODEL_PATH: str = config("DEFAULT_MODEL_PATH")

DB_URL: str = config("DB_URL")
DB_USERNAME: str = config("DB_USERNAME")
DB_PASSWORD: str = config("DB_PASSWORD")
MAX_CONNECTIONS_COUNT: int = config("MAX_CONNECTIONS_COUNT", cast=int, default=10)
MIN_CONNECTIONS_COUNT: int = config("MIN_CONNECTIONS_COUNT", cast=int, default=10)

ALLOWED_HOSTS: List[str] = config(
    "ALLOWED_HOSTS", cast=CommaSeparatedStrings, default="",
)
LOGGING_LEVEL = logging.DEBUG if IS_DEBUG else logging.INFO
LOGGERS = ("uvicorn.asgi", "uvicorn.access")

logging.getLogger().handlers = [InterceptHandler()]
for logger_name in LOGGERS:
    logging_logger = logging.getLogger(logger_name)
    logging_logger.handlers = [InterceptHandler(level=LOGGING_LEVEL)]

logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])
