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
from datetime import datetime

from .Plugin import Plugin, Version


class SpigetVersion(Version):
    def __init__(self, name: str, version: str, date: datetime, version_id: int):
        super().__init__(name=name, version=version, date=date)
        self.version_id = version_id


class SpigetPlugin(Plugin):
    _base_url = "https://api.spiget.org/v2"

    type = "spiget"

    def get_latest_version_info(self):
        url = f"{self._base_url}/resources/{self._resource}/versions/latest"
        response = self._get(url)
        response.raise_for_status()
        json = response.json()
        version = SpigetVersion.from_timestamp(
            name=json["name"],
            date=json["releaseDate"],
            version=json["name"],
            version_id=json["id"],
        )
        return version

    def download_url(self, version: SpigetVersion) -> str:
        return f"{self._base_url}/resources/{self._resource}/versions/{version.version_id}/download"
