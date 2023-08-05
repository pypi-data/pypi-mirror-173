from inspect import getfile
from typing import Callable, Union

import pkg_resources
from click import Command, Group, Option


def version_option(
) -> Callable[[Union[Command, Group, Callable[..., None]]], Union[Command, Group, Callable[..., None], Callable]]:
    """Click Option Decorator to define a global option for cli decorator."""

    def global_option_decorator(option_func: Union[Union[Command, Group], Callable[..., None]]):
        if not callable(option_func):
            return option_func

        name = option_func.__qualname__
        module = getfile(option_func)
        version = "0.0.1"

        if hasattr(option_func, "__module__"):
            module = option_func.__module__.split(".", 1)[0]
            if module != "__main__":
                version = pkg_resources.get_distribution(module).version

        if not hasattr(option_func, "params"):
            option_func.params = []
        option_func.params.append(_option)

        return option_func

    return global_option_decorator
