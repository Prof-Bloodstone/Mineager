from pathlib import Path

import click

from .config import Config, YamlConfig
from .plugins.PluginLoader import PLUGIN_CLASSES, get_plugin


class ConfigContext:
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


supported_plugins = [m.type for m in PLUGIN_CLASSES]


def is_plugin_in_config(config: Config, type: str, name: str, resource: str):
    if name in {p.name for p in config.get_plugins()}:
        return True
    return resource in {p.resource for p in config.get_plugins() if p.type == type}


def add_options(options):
    """Adds given options to decorated function"""

    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func

    return _add_options


# Common options
# Options used for specifying plugin on the command line
OPTIONS_ADD_PLUGIN = [
    click.option(
        "--type",
        type=click.Choice(supported_plugins, case_sensitive=False),
        required=True,
        help="The type of the plugin source.",
    ),
    click.option(
        "--name", type=str, required=True, help="The local name for the plugin."
    ),
    click.option(
        "--resource",
        type=str,
        required=True,
        help="The resource identifier. See documentation for details.",
    ),
]
