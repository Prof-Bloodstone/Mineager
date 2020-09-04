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
import click

from ...plugins.PluginLoader import get_plugin
from ..cli_utils import ConfigContext, add_options, assert_plugin_not_in_config
from .utils import OPTIONS_MANUALLY_ADD_PLUGIN, try_install_plugin


@click.group("manual")
@add_options(OPTIONS_MANUALLY_ADD_PLUGIN)
def manual_plugin_cmd():
    """Manually add/install plugins."""
    raise click.ClickException("Manual plugin management is temporarily disabled")


@manual_plugin_cmd.command()
@click.pass_obj
def add(cctx: ConfigContext, type: str, name: str, resource: str):
    """
    Manually add given plugin to config file.
    No verification is being done.
    """
    plugin = get_plugin(type)(name, resource)
    assert_plugin_not_in_config(cctx.config, plugin)
    cctx.config.add_plugin(plugin)
    cctx.config.save()


@manual_plugin_cmd.command()
@click.pass_context
def install(ctx: click.Context, type: str, name: str, resource: str):
    """Manually add and install the plugin."""
    cctx: ConfigContext = ctx.obj
    plugin = get_plugin(type)(name, resource)
    assert_plugin_not_in_config(cctx.config, plugin)
    try_install_plugin(ctx, plugin)
    cctx.config.add_plugin(plugin)
    cctx.config.save()
