#!/usr/bin/env python3
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

from .cli.cli_utils import ConfigContext
from .cli.plugin.commands import plugin_cmd


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


cli.add_command(plugin_cmd)

if __name__ == "__main__":
    cli()
