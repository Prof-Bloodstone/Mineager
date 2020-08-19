from typing import Union

import click
from requests import HTTPError

from ... import ManualDownloadRequired, UrlParser
from ...plugins import Plugin
from ..cli_utils import CLIColors, URLArgument, supported_plugins


def try_install_plugin(ctx: click.Context, plugin: Plugin) -> None:
    try:
        version = plugin.get_latest_version_info()
        click.secho(
            f"Installing {plugin.name}, version: {version.version}",
            fg=CLIColors.INFO.value,
        )
        try:
            plugin.download(version)
        except ManualDownloadRequired as e:
            raise click.ClickException(
                f"Failed to download {plugin.name} - try downloading it manually from {e.url} and adding it using: "
                f"{ctx.parent.command_path} manual add --name {plugin.name!r} --type {type!r} --resource {plugin.resource!r}"
            )
    except HTTPError as e:
        raise click.ClickException(str(e)) from e


def get_plugin_from_url(url: str, name: Union[str, None]) -> Plugin:
    plugin = UrlParser.parse(url)
    if name:
        try:
            plugin.name = name
        except ValueError as e:
            raise click.ClickException(f"Invalid custom name: {name!r}",) from e
    return plugin


def get_name_option(required: bool) -> click.Option:
    return click.option(
        "--name",
        type=str,
        required=required,
        help="The local name for the plugin.",
        metavar="<name>",
    )


# Common options
# Options used for specifying plugin on the command line
OPTIONS_MANUALLY_ADD_PLUGIN = [
    click.option(
        "--type",
        type=click.Choice(supported_plugins, case_sensitive=False),
        required=True,
        help="The type of the plugin source.",
        metavar="<type>",
    ),
    get_name_option(required=True),
    click.option(
        "--resource",
        type=str,
        required=True,
        help="The resource identifier. See documentation for details.",
        metavar="<resource>",
    ),
]

OPTIONS_ADD_PLUGIN = [
    click.argument("url", type=URLArgument(), required=True),
    get_name_option(required=False),
]
