__all__ = ['__version__']

import sys

from dynaconf import Dynaconf, Validator
from loguru import logger
import pbr.version

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

version_info = pbr.version.VersionInfo('timonctl')
# We have a circular import problem when we first run python setup.py sdist
# It's harmless, so deflect it.
try:
    __version__ = version_info.version_string()
except AttributeError:
    __version__ = None
