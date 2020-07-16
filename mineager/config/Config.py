from abc import ABC, abstractmethod
from pathlib import Path

from mineager.plugins import PluginLoader


class Config(ABC):
    def __init__(this, file: Path):
        this._file = file
        assert file.exists()

    @abstractmethod
    def load(this):
        pass

    @abstractmethod
    def save(this):
        pass

    @staticmethod
    def parse_plugins(data):
        plugins = []
        for index, entry in enumerate(data):
            type_name = entry.pop('type', None)
            if type_name is None:
                raise ValueError(f"Required key 'type' is missing in entry {index+1}")
            plugin = PluginLoader.get_plugin(type_name)(**entry)
            plugins.append(plugin)
        return plugins
