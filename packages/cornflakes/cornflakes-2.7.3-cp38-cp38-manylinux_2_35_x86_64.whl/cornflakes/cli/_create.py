from click import style, version_option
import pkg_resources

from cornflakes.click import group, command, Console, RichGroup
from cornflakes.logging import logger


@group("create")
@version_option(
    prog_name="cornflakes",
    version=pkg_resources.get_distribution("cornflakes").version,
    message=style(
        f"\033[95m{'cornflakes'}\033"
        f"[0m \033[95mVersion\033[0m: \033[1m"
        f"{pkg_resources.get_distribution('cornflakes').version}\033[0m"
    ),
)
def create_new_config():
    """Create config template."""
    pass


@command("test")
def test(parent: RichGroup):
    """Test click."""
    logger.info("call create")
    logger.debug("debug log?")
    for _ in range(10):
        parent.console.print("[blue]blub")

    with open("/home/sgeist/arbeit/cornflakes/test.txt", "wb") as f:
        f.write(b"blub\n")


create_new_config.add_command(test)
