import click

from ...plugins.PluginLoader import get_plugin
from ..cli_utils import ConfigContext, add_options, assert_plugin_not_in_config
from .utils import OPTIONS_MANUALLY_ADD_PLUGIN, try_install_plugin


@click.group("manual")
@add_options(OPTIONS_MANUALLY_ADD_PLUGIN)
def manual_plugin_cmd():
    """Manually add/install plugins."""


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
