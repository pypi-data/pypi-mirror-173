from functools import wraps
from inspect import isclass
import logging
import logging.config
import os
from types import FunctionType
from typing import Any, Callable, Optional, Protocol, Union

import yaml


def setup_logging(
    default_path: str = "logging.yaml",
    default_level: Optional[int] = logging.WARNING,
    env_key: str = "LOG_CFG",
    force: bool = True,
):
    """Setup logging configuration.

    :param default_path: Default path to logging config file.
    :param default_level: Default log-level (Logging.INFO).
    :param env_key: Environment key to use for logging configuration.
    :param force: Force logging configuration.
    """
    if value := os.getenv(env_key, None):
        default_path = value

    if default_level:
        default_level = default_level

    if os.path.exists(default_path):
        with open(default_path) as f:
            config = yaml.safe_load(f.read())
        if default_level:
            for handler in config["root"]["handlers"]:
                config["handlers"][handler]["level"] = default_level
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(
            level=default_level,
            format="%(asctime)s - %(name)s - %(funcName)s()  - (%(pathname)s:%(lineno)d) - %(levelname)s - %(message)s",
            filename="default.log",
            filemode="w",
        )
    logging.getLogger().setLevel(default_level)


setup_logging = setup_logging


class LoggerMetaClass(Protocol):
    """LoggerMetaClass used for Type Annotation."""

    logger: logging.Logger = None


def attach_log(
    obj,
    log_level: int = logging.WARNING,
    default_level: int = None,
    default_path: str = "logging.yaml",
    env_key: str = "LOG_CFG",
) -> Union[Callable[..., Any], LoggerMetaClass]:
    """Function decorator to attach Logger to functions.

    :param obj: Logger function or class to attach the logging to.
    :param log_level: log-level for the current object logging.
    :param default_path: Default path to logging config file.
    :param default_level: Default log-level (Logging.INFO).
    :param env_key: Environment key to use for logging configuration.

    :returns: Object with attached logging instance
    """
    if isclass(obj):
        obj.logger = logging.getLogger(obj.__name__)
        obj.logger.setLevel(log_level)
        if default_level:
            setup_logging(default_path, default_level, env_key, force=True)

        if log_level == logging.DEBUG:
            for attribute_name, attribute in obj.__dict__.items():
                if isinstance(attribute, FunctionType):
                    # replace it with a wrapped version
                    attribute = attach_log(obj=attribute)
                    setattr(obj, attribute_name, attribute)
        return obj

    if log_level != logging.DEBUG or not callable(obj):
        return obj

    @wraps(obj)
    def wrapper(*args, **kwargs):
        call_signature = ", ".join([repr(a) for a in args] + [f"{k}={v!r}" for k, v in kwargs.items()])
        logging.debug(f"function {obj.__name__} called with args {call_signature}")
        try:
            return obj(*args, **kwargs)
        except Exception as e:
            logging.exception(f"Exception raised in {obj.__name__}. exception: {str(e)}")
            raise e

    return wrapper
