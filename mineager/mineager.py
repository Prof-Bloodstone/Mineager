#!/usr/bin/env python3
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
