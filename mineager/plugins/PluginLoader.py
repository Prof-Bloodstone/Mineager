from typing import Type

from . import GithubPlugin, Plugin, SpigetPlugin

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
