import sys

from dynaconf import Dynaconf, Validator
from loguru import logger

settings = Dynaconf(
    envvar_prefix="TIMON",
    settings_files=["timon.yaml"]
)
settings.validators.register(
    Validator("LOG_LEVEL", default="INFO"),
    Validator("JWT_ALGORITHM", default="HS256"),
    Validator("JWT_SECRET", default="BC49896D-3B39-4FD2-93BE-38C3A12D200A")
)
settings.validators.validate_all()

logger.remove()
logger.add(sys.stderr, level=settings.log_level)
