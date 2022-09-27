from dynaconf import Dynaconf
from loguru import logger  # noqa F401

settings = Dynaconf(
    envvar_prefix="TIMON",
    settings_files=["timon.yaml"]
)
