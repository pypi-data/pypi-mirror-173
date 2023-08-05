from inspect import getfile
from typing import Callable

from click import Group
import pkg_resources

from cornflakes.click import RichConfig, group, style, version_option


def cli(*args, callback: Callable = None, **kwargs):
    """Function that creates generic click CLI Object."""

    def cli_wrapper(w_callback: Callable) -> Callable[..., Group]:
        if not callable(w_callback):
            return w_callback

        name = w_callback.__qualname__
        module = getfile(w_callback)
        version = "0.0.1"

        if hasattr(w_callback, "__module__"):
            module = w_callback.__module__.split(".", 1)[0]
            if module != "__main__":
                version = pkg_resources.get_distribution(module).version

        config = RichConfig(*args, **kwargs)

        cli_group = version_option(
            prog_name=name,
            version=version,
            message=style(f"\033[95m{module}\033" f"[0m \033[95mVersion\033[0m: \033[1m" f"{version}\033[0m"),
        )(group(module.split(".", 1)[0], config=config)(w_callback))

        if cli_group.config.GLOBAL_OPTIONS:
            for option_obj in cli_group.config.GLOBAL_OPTIONS:
                cli_group.params.extend(option_obj.params)
        if config.CONTEXT_SETTINGS:
            cli_group.context_settings = config.CONTEXT_SETTINGS
        return cli_group

    if callback:
        return cli_wrapper(callback, *args, **kwargs)
    return cli_wrapper
