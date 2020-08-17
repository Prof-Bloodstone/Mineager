from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

from ..plugins import Plugin, PluginLoader
from ..types import CONFIG, PLUGIN_LIST


class Config(ABC):
    def __init__(self, file: Path):
        self._file = file
        self._data = None

    @property
    def data(self):
        return self._data

    @abstractmethod
    def _load(self) -> CONFIG:
        pass

    def load(self, required=False):
        if self._file.exists():
            self._data = self._load()
        elif not required:
            self._data = {}
        else:
            raise FileNotFoundError(self._file.name)

    @abstractmethod
    def save(self):
        pass

    def get_plugins(self) -> PLUGIN_LIST:
        return self.parse_plugins()

    def parse_plugins(self):
        plugins = []
        plugins_data = self.data.get("plugins", None)
        if plugins_data is None:
            raise ValueError('Missing top-level key "plugins"')
        for index, entry in enumerate(plugins_data):
            entry = entry.copy()
            type_name = entry.pop("type", None)
            if type_name is None:
                raise ValueError(f"Required key 'type' is missing in entry {index+1}")
            plugin = PluginLoader.get_plugin(type_name)(**entry)
            plugins.append(plugin)
        return plugins

    @staticmethod
    def serialize_plugin(plugin: Plugin):
        # TODO: probably should move this logic into plugin itself
        fields = (
            "type",
            "name",
            "resource",
        )
        return {field: getattr(plugin, field) for field in fields}

    def add_plugin(self, plugin: Plugin):
        plugins_data: List = self.data.get("plugins", [])
        plugins_data.append(self.serialize_plugin(plugin))
        self.data["plugins"] = plugins_data
