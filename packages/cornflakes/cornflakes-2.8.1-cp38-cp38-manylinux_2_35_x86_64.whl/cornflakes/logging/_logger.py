from functools import wraps
from inspect import isclass
import logging
import logging.config
import os
from types import FunctionType
from typing import Any, Callable, Optional, Union, Protocol

import yaml


def setup_logging(
        default_path: str = "logging.yaml",
        default_level: Optional[int] = None,
        env_key: str = "LOG_CFG",
        force: bool = False
):
    """Setup logging configuration.

    :param force: Overwrite current log-level
    :param default_path: Default path to logging config file.
    :param default_level: Default log-level (Logging.INFO).
    :param env_key: Environment key to use for logging configuration.
    """
    if value := os.getenv(env_key, None):
        default_path = value

    if os.path.exists(default_path):
        with open(default_path) as f:
            config = yaml.safe_load(f.read())
            if default_level and force:
                for handler in config["root"]["handlers"]:
                    config["handlers"][handler]["level"] = default_level
            logging.config.dictConfig(config)
    else:
        logging.basicConfig(
            level=default_level,
            format="%(asctime)s - %(name)s - %(funcName)s()  - (%(pathname)s:%(lineno)d) - %(levelname)s - %(message)s"
        )


class LoggerMetaClass(Protocol):
    """LoggerMetaClass used for Type Annotation."""
    logger: logging.Logger = None


# def attach_log(

def attach_log(
        obj,
        log_level: int = None,
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
    def obj_wrapper(w_obj):
        if isclass(w_obj):
            w_obj.logger = logging.getLogger(w_obj.__name__)
            if log_level:
                w_obj.logger.setLevel(log_level)
            if default_level:
                setup_logging(default_path, default_level, env_key, force=True)

            if w_obj.logger.level == logging.DEBUG:
                for attribute_name, attribute in w_obj.__dict__.items():
                    if isinstance(attribute, FunctionType):
                        # replace it with a wrapped version
                        attribute = attach_log(obj=attribute, log_level=log_level,
                                               default_level=default_level,
                                               default_path=default_path, env_key=env_key)
                        setattr(w_obj, attribute_name, attribute)
            return w_obj

        if callable(w_obj):
            __logger = logging.getLogger(w_obj.__qualname__.rsplit(".", 1)[0])

            if __logger.level != logging.DEBUG:
                return w_obj

            @wraps(w_obj)
            def wrapper(*args, **kwargs):
                call_signature = ", ".join([repr(a) for a in args] + [f"{k}={v!r}" for k, v in kwargs.items()])
                __logger.debug(f"function {w_obj.__name__} called with args {call_signature}")
                try:
                    return w_obj(*args, **kwargs)
                except Exception as e:
                    __logger.exception(f"Exception raised in {w_obj.__name__}. exception: {str(e)}")
                    raise e

            return wrapper

    if not obj:
        return obj_wrapper
    return obj_wrapper(obj)
