#
# Copyright (C) 2020 Prof_Bloodstone.
#
# This file is part of mineager
# (see https://github.com/Prof-Bloodstone/Mineager).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

from ..data_types import CONFIG, PLUGIN_LIST
from ..plugins import Plugin, PluginLoader


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
            self._data = {'plugins': []}
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
        return dict(type=plugin.type, **plugin.serialize())

    def add_plugin(self, plugin: Plugin):
        plugins_data: List = self.data.get("plugins", [])
        plugins_data.append(self.serialize_plugin(plugin))
        self.data["plugins"] = plugins_data
