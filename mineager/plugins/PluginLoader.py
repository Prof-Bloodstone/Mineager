from typing import Iterable, Type

from .GithubPlugin import GithubPlugin
from .Plugin import Plugin
from .SpigetPlugin import SpigetPlugin

PLUGIN_CLASSES: Iterable[Type[Plugin]] = (
    SpigetPlugin,
    GithubPlugin,
)


def get_plugin(name: str) -> Type[Plugin]:
    name = name.lower()
    for cls in PLUGIN_CLASSES:
        if name == cls.type:
            return cls

    ValueError(name)
