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
from typing import NamedTuple

from ..utils import common_start_substring
from .Plugin import InvalidPluginSourceException, Plugin, Version


class WithCommonPrefix(NamedTuple):
    prefix: str
    original: str


class JenkinsVersion(Version):
    def __init__(
        self, name: str, version: str, date: datetime, download_url: str,
    ):
        super().__init__(name, version, date)
        self.download_url = download_url


class JenkinsPlugin(Plugin):
    _datetime_format = "%Y-%m-%dT%H:%M:%SZ"

    type = "jenkins"

    def __init__(self, name: str, resource: str, url: str):
        """resource should be a name of jar to download - will use the "closest" one"""
        super().__init__(name=name, resource=resource)
        self._url = url

    @property
    def url(self):
        return self._url

    def _get_api_url(self, url: str):
        return f"{url}/api/json"

    def get_latest_version_info(self) -> JenkinsVersion:
        url = self._get_api_url(self.url)
        response = self._get(url)
        response.raise_for_status()
        json = response.json()
        builds = json.get("builds")
        if not builds or len(builds) == 0:
            raise InvalidPluginSourceException(
                f"Looks like {self.url} doesn't have any builds!"
            )
        latest_build = builds[0]
        latest_url = latest_build["url"]

        response = self._get(self._get_api_url(latest_url))
        response.raise_for_status()
        json = response.json()

        artifacts = json.get("artifacts")
        if (
            not artifacts
            or len(artifacts) == 0
            or not any(art["fileName"].endswith(".jar") for art in artifacts)
        ):
            raise InvalidPluginSourceException(
                f"Looks like {latest_url} does not have any artifacts"
            )

        jar_files = (
            art["relativePath"] for art in artifacts if art["fileName"].endswith(".jar")
        )

        paths_with_common_prefixes = (
            WithCommonPrefix(common_start_substring(self.resource, path), path)
            for path in jar_files
        )
        file_path = sorted(
            paths_with_common_prefixes, key=lambda x: len(x.prefix), reverse=True
        )[0]

        version = JenkinsVersion.from_timestamp(
            name=self._name,
            version=latest_build["number"],
            date=json["timestamp"] // 1000,  # It's in ms
            download_url=f"{latest_url}/{file_path.original}",
        )
        return version

    def download_url(self, version: JenkinsVersion) -> str:
        return version.download_url
