from collections import namedtuple
from enum import Enum
from pathlib import Path
from urllib.parse import urlparse

import click

from ..config import Config, YamlConfig
from ..plugins import PLUGIN_CLASSES, Plugin


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


class CLIColors(Enum):
    # TODO: Decide on colors
    UP_TO_DATE = "green"
    NEW = "yellow"
    UPDATE_AVAILABLE = "red"
    WARNING = "bright_yellow"
    ERROR = "red"
    INFO = "yellow"


def is_plugin_in_config(config: Config, plugin: Plugin):
    if plugin.name in {p.name for p in config.get_plugins()}:
        return True
    return plugin.resource in {
        p.resource for p in config.get_plugins() if p.type == plugin.type
    }


# TODO: Add this to a "proxy" config context, so that in doesn't have to be executed manually each time
def assert_plugin_not_in_config(config: Config, plugin: Plugin):
    if is_plugin_in_config(config=config, plugin=plugin):
        raise click.ClickException(
            f"A plugin with name '{plugin.name}' already exists!"
        )


class URLArgument(click.ParamType):
    name = "url"

    def convert(self, value, param, ctx):
        url = value
        try:
            url = url if urlparse(url).netloc != "" else f"//{url}"
        except TypeError:
            self.fail(
                "expected string for url conversion, "
                f"got {value!r} of type {type(value).__name__}",
                param,
                ctx,
            )
        parsed_url = urlparse(url)
        if parsed_url.netloc != "" and parsed_url.path != "":
            return url
        self.fail(f"{value!r} is not a valid URL", param, ctx)


PluginDownloadReason = namedtuple("PluginDownloadReason", ["plugin", "reason"])


def add_options(options):
    """Adds given options to decorated function"""

    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func

    return _add_options
