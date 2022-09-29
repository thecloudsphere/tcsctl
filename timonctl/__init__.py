import sys

from dynaconf import Dynaconf, Validator
from loguru import logger  # noqa F401

settings = Dynaconf(
    envvar_prefix="TIMON",
    settings_files=["timon.yaml"]
)
settings.validators.register(
    Validator("LOG_LEVEL", default="INFO")
)
settings.validators.validate_all()

logger.remove()
logger.add(sys.stderr, level=settings.log_level)
