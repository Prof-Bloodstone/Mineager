#!/usr/bin/env python3
from .config import Config, YamlConfig
from .plugins.PluginLoader import PLUGIN_CLASSES, get_plugin
from requests import HTTPError
from pathlib import Path
from .utils import CLIColors
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
        self._config = YamlConfig(self.config_path)
        self._config.load()

    @property
    def config(self) -> Config:
        return self._config


pass_context = click.make_pass_decorator(Context)
supported_plugins = [m.type for m in PLUGIN_CLASSES]


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
@click.option(
    "--type",
    type=click.Choice(supported_plugins, case_sensitive=False),
    required=True,
    help="The type of the plugin source.",
)
@click.option("--name", type=str, required=True, help="The local name for the plugin.")
@click.option(
    "--resource",
    type=str,
    required=True,
    help="The resource identifier. See documentation for details.",
)
@pass_context
def install(ctx: Context, type: str, name: str, resource: str):
    """Installs a plugin."""
    plugin = get_plugin(type)(name, resource)
    try:
        version = plugin.get_latest_version_info()
        click.echo(f"Installing {name}, version: {version.version}")
        plugin.download(version)
    except HTTPError as e:
        click.echo(e, err=True)
        return

    ctx.config.add_plugin(plugin)
    ctx.config.save()


@cli.command()
@pass_context
def status(ctx: Context):
    """Shows the current status between on-disk and remote state."""  # TODO
    for plugin in ctx.config.get_plugins():
        latest_version = plugin.get_latest_version_info()
        current_version = plugin.version_from_file()
        msg = f"{plugin.name} {latest_version.version} was released at {latest_version.date}"
        if current_version is None:
            color = CLIColors.NEW
        else:
            msg = f"{msg} - current version is {current_version.version}, downloaded at {current_version.date}"
            color = (
                CLIColors.UPDATE_AVAILABLE
                if current_version < latest_version
                else CLIColors.UP_TO_DATE
            )
        click.secho(msg, fg=color.value)


@cli.command()
@pass_context
def download(ctx: Context):
    """Download newest available version of all the plugins."""
    for plugin in ctx.config.get_plugins():
        current_version = plugin.version_from_file()
        latest_version = plugin.get_latest_version_info()
        if current_version is None or current_version < latest_version:
            click.echo(f"Downloading {plugin.name}")
            plugin.download()


if __name__ == "__main__":
    cli()
