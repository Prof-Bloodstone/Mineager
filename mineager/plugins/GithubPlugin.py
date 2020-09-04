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


class GithubVersion(Version):
    def __init__(
        self,
        name: str,
        version: str,
        date: datetime,
        release_id: int,
        download_url: str,
    ):
        super().__init__(name, version, date)
        self.release_id = release_id
        self.download_url = download_url


class GithubPlugin(Plugin):
    _base_url = "https://api.github.com/repos"
    _datetime_format = "%Y-%m-%dT%H:%M:%SZ"

    type = "github"

    def get_latest_version_info(self):
        url = f"{self._base_url}/{self._resource}/releases/latest"
        response = self._get(url)
        response.raise_for_status()
        json = response.json()
        release_asset = next(
            (
                asset
                for asset in json["assets"]
                if asset["name"].lower() == f"{self._name.lower()}.jar"
            ),
            None,
        )
        assert release_asset is not None  # TODO: Throw a proper exception
        version = GithubVersion(
            name=self._name,
            version=json["tag_name"],
            date=datetime.strptime(json["published_at"], self._datetime_format),
            release_id=json["id"],
            download_url=release_asset["browser_download_url"],
        )
        return version

    def download_url(self, version: GithubVersion) -> str:
        return version.download_url
