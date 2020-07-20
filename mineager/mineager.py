#!/usr/bin/env python3
from mineager.config import YamlConfig
from pathlib import Path
from .types import PLUGIN_LIST
import click


class Context:
    def __init__(self, config_path):
        self.config_path: Path = config_path

    @property
    def config_path(self) -> Path:
        return self._config_path

    @config_path.setter
    def config_path(self, value) -> None:
        if not isinstance(value, Path):
            if isinstance(value, str):
                value = Path(value)
            else:
                raise ValueError(f"{value!r} is not a valid type!")
        self._config_path = value

    @property
    def data(self) -> PLUGIN_LIST:
        return YamlConfig(self.config_path).get_plugins()


pass_context = click.make_pass_decorator(Context)


@click.group()
@click.option(
    "--config-path",
    envvar="MINEAGER_CONFIG_PATH",
    default="mineager.yml",
    metavar="PATH",
    help="Changes the config location.",
    type=click.Path(),
)
@click.pass_context
def cli(ctx, config_path: str):
    """Command-line tool to manage plugins on your Minecraft server."""
    ctx.obj = Context(config_path)


@cli.command()
@pass_context
def status(ctx: Context):
    """Shows the current status between on-disk and remote state."""  # TODO
    for plugin in ctx.data:
        info = plugin.get_latest_version_info()
        current_version = plugin.version_from_file()
        click.echo(f"{plugin.name} {info.version} was released at {info.date} - current version is {current_version.version}, downloaded at {current_version.date}")


@cli.command()
@pass_context
def download(ctx: Context):
    """Download newest available version of all the plugins."""
    for plugin in ctx.data:
        click.echo(f"Downloading {plugin.name}")
        plugin.download()


if __name__ == "__main__":
    cli()
