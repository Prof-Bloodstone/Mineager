from typing import List

import yaml

from mineager.plugins import Plugin

from . import Config

try:
    from yaml import CDumper as Dumper
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Dumper, Loader


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
