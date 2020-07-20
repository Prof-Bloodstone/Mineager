from abc import ABC, abstractmethod
from pathlib import Path


from ..plugins import PluginLoader
from ..types import CONFIG, PLUGIN_LIST


class Config(ABC):
    def __init__(self, file: Path):
        self._file = file

    @abstractmethod
    def load(self) -> CONFIG:
        pass

    @abstractmethod
    def save(self, data: CONFIG):
        pass

    def get_plugins(self) -> PLUGIN_LIST:
        return self.parse_plugins(self.load())

    @staticmethod
    def parse_plugins(data: CONFIG):
        plugins = []
        plugins_data = data.get('plugins', None)
        if plugins_data is None:
            raise ValueError('Missing top-level key "plugins"')
        for index, entry in enumerate(plugins_data):
            type_name = entry.pop('type', None)
            if type_name is None:
                raise ValueError(f"Required key 'type' is missing in entry {index+1}")
            plugin = PluginLoader.get_plugin(type_name)(**entry)
            plugins.append(plugin)
        return plugins
