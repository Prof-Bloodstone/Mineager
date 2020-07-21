from . import Config
from mineager.plugins import Plugin

from typing import List

import yaml

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


class YamlConfig(Config):
    def _load(self) -> List[Plugin]:
        with self._file.open("r") as stream:
            return yaml.load(stream, Loader=Loader)

    def save(self) -> None:
        dump = yaml.dump(
            self.data,
            Dumper=Dumper,
            # Always use block-styled instead of collection-styled dump
            default_flow_style=False,
        )
        with self._file.open("w") as f:
            f.write(dump)