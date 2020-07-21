
from . import Plugin, SpigetPlugin, GithubPlugin

from typing import Type, Tuple


PLUGIN_CLASSES = (
    SpigetPlugin,
    GithubPlugin,
)


def get_plugin(name: str) -> Type[Plugin]:
    name = name.lower()
    for cls in PLUGIN_CLASSES:
        if name == cls.type:
            return cls

    ValueError(name)
