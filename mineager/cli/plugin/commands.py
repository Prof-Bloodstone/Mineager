#
# Copyright (C) 2020 Prof_Bloodstone.
#
# This file is part of mineager
# (see https://github.com/Prof-Bloodstone/Mineager).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#
from typing import Union

import click

from ... import ManualDownloadRequired
from ..cli_utils import (
    CLIColors,
    ConfigContext,
    PluginDownloadReason,
    add_options,
    assert_plugin_not_in_config,
)
from .manual_commands import manual_plugin_cmd
from .utils import OPTIONS_ADD_PLUGIN, get_plugin_from_url, try_install_plugin


@click.group("plugin")
def plugin_cmd():
    """Manage plugins."""


plugin_cmd.add_command(manual_plugin_cmd)


@plugin_cmd.command()
@add_options(OPTIONS_ADD_PLUGIN)
@click.pass_obj
def add(cctx: ConfigContext, url: str, name: Union[str, None]):
    """Add plugin source based on given URL"""
    plugin = get_plugin_from_url(url, name)
    assert_plugin_not_in_config(cctx.config, plugin)
    cctx.config.add_plugin(plugin)
    cctx.config.save()


@plugin_cmd.command()
@add_options(OPTIONS_ADD_PLUGIN)
@click.pass_obj
def install(ctx: click.Context, url: str, name: Union[str, None]):
    """Add and install plugin source based on given URL"""
    cctx: ConfigContext = ctx.obj
    plugin = get_plugin_from_url(url, name)
    assert_plugin_not_in_config(cctx.config, plugin)
    try_install_plugin(ctx, plugin)
    cctx.config.add_plugin(plugin)
    cctx.config.save()


@plugin_cmd.command()
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


@plugin_cmd.command()
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
    with click.progressbar(to_download, label="Downloading") as bar:
        for (plugin, reason) in bar:
            download_reason = "Updating" if reason == "update" else "Downloading"
            bar.label = f"{download_reason} {plugin.name}"
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
