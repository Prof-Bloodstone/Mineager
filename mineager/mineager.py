#!/usr/bin/env python3
import click
from requests import HTTPError

from mineager import ManualDownloadRequired

from .cli_utils import (
    OPTIONS_ADD_PLUGIN,
    ConfigContext,
    add_options,
    is_plugin_in_config,
)
from .plugins.PluginLoader import get_plugin
from .utils import CLIColors, PluginDownloadReason


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
    ctx.obj = ConfigContext(config_path)


@cli.command()
@add_options(OPTIONS_ADD_PLUGIN)
@click.pass_obj
def add(ctx: ConfigContext, type: str, name: str, resource: str):
    """
    Manually add given plugin to config file.
    No verification is being done.
    """
    if is_plugin_in_config(ctx.config, type=type, name=name, resource=resource):
        raise click.ClickException(
            click.style(
                f"A plugin with name '{name}' already exists!", fg=CLIColors.ERROR.value
            )
        )
    plugin = get_plugin(type)(name, resource)
    ctx.config.add_plugin(plugin)
    ctx.config.save()


@cli.command()
@add_options(OPTIONS_ADD_PLUGIN)
@click.pass_context
def install(cctx: click.Context, type: str, name: str, resource: str):
    """Installs a plugin."""
    ctx: ConfigContext = cctx.obj
    if is_plugin_in_config(ctx.config, type=type, name=name, resource=resource):
        raise click.ClickException(
            click.style(
                f"A plugin with name '{name}' already exists!", fg=CLIColors.ERROR.value
            )
        )
    plugin = get_plugin(type)(name, resource)
    try:
        version = plugin.get_latest_version_info()
        click.echo(f"Installing {name}, version: {version.version}")
        try:
            plugin.download(version)
        except ManualDownloadRequired as e:
            click.secho(
                f"Failed to download {plugin.name} - try downloading it manually from {e.url} and adding it using: "
                f"{cctx.parent.command_path} add --name {name!r} --type {type!r} --resource {resource!r}",
                fg=CLIColors.WARNING.value,
            )
            return 1
    except HTTPError as e:
        click.echo(e, err=True)
        return 1

    ctx.config.add_plugin(plugin)
    ctx.config.save()


@cli.command()
@click.pass_obj
def status(cctx: ConfigContext):
    """Shows the current status between on-disk and remote state."""
    for plugin in cctx.config.get_plugins():
        latest_version = plugin.get_latest_version_info()
        current_version = plugin.version_from_file()
        msg = f"{plugin.name} {latest_version.version} was released at {latest_version.date}"
        if current_version is None:
            color = CLIColors.NEW
            msg = f"{msg} - Not Installed"
        else:
            msg = f"{msg} - current version is {current_version.version}, downloaded at {current_version.date}"
            color = (
                CLIColors.UPDATE_AVAILABLE
                if current_version < latest_version
                else CLIColors.UP_TO_DATE
            )
        click.secho(msg, fg=color.value)


@cli.command()
@click.pass_obj
def update(cctx: ConfigContext):
    """Download newest available version of all plugins listed in config."""
    to_download = []
    for plugin in cctx.config.get_plugins():
        current_version = plugin.version_from_file()
        latest_version = plugin.get_latest_version_info()
        if current_version is None:
            to_download.append(PluginDownloadReason(plugin, "download"))
        elif current_version < latest_version:
            to_download.append(PluginDownloadReason(plugin, "update"))
    if not to_download:
        click.secho("Everything is up to date!", fg=CLIColors.UP_TO_DATE.value)
        return
    to_manually_download = []
    with click.progressbar(to_download) as bar:
        for (plugin, reason) in bar:
            download_reason = "Updating" if reason == "update" else "Downloading"
            click.echo(f"{download_reason} {plugin.name}")
            try:
                plugin.download()
            except ManualDownloadRequired as e:
                to_manually_download.append(
                    (PluginDownloadReason(plugin, reason), e.url)
                )
    if to_manually_download:
        click.secho(
            "Failed to download some plugins automatically - try doing so manually:",
            fg=CLIColors.WARNING.value,
        )
        for ((plugin, reason), url) in to_manually_download:
            click.echo(f"{plugin.name}: {url}")


if __name__ == "__main__":
    cli()
