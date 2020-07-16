from . import Config
from mineager.plugins import Plugin

from typing import List

import yaml

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


class YamlConfig(Config):
    def load(self) -> List[Plugin]:
        with self._file.open("r") as stream:
            data = yaml.load(stream, Loader=Loader)
        return self.parse_plugins(data)

    def save(self, data) -> None:
        dump = yaml.dump(
            data,
            Dumper=Dumper,
            # Always use block-styled instead of collection-styled dump
            default_flow_style=False,
        )
        with self._file.open("w") as f:
            f.write(dump)
