
from . import Plugin, SpigetPlugin, GithubPlugin

from typing import Type


def get_plugin(name: str) -> Type[Plugin]:
    name = name.lower()
    if name in ('spiget', 'spigot'):
        return SpigetPlugin
    elif name == 'github':
        return GithubPlugin
    else:
        ValueError(name)
