from typing import Iterable, Type

from .GithubPlugin import GithubPlugin
from .JenkinsPlugin import JenkinsPlugin
from .Plugin import Plugin
from .SpigetPlugin import SpigetPlugin

PLUGIN_CLASSES: Iterable[Type[Plugin]] = (
    SpigetPlugin,
    GithubPlugin,
    JenkinsPlugin,
)


def get_plugin(name: str) -> Type[Plugin]:
    name = name.lower()
    for cls in PLUGIN_CLASSES:
        if name == cls.type:
            return cls
    raise ValueError(f"Unable to find plugin of type {name}")
