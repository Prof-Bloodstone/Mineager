
from typing import List, Dict

from .plugins import Plugin

PLUGIN_LIST = List[Plugin]

CONFIG_PLUGIN = Dict[str, str]
CONFIG_PLUGIN_LIST = List[CONFIG_PLUGIN]

CONFIG = Dict[str, CONFIG_PLUGIN_LIST]
