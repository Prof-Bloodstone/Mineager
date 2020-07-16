from .Plugin import Plugin, Version
from datetime import datetime


class SpigetVersion(Version):
    def __init__(self, name: str, date: datetime, version_id: int):
        super().__init__(name, date)
        self.version_id = version_id


class SpigetPlugin(Plugin):
    _base_url = "https://api.spiget.org/v2"

    def get_latest_version_info(self):
        url = f"{self._base_url}/resources/{self._resource}/versions/latest"
        response = self._get(url)
        response.raise_for_status()
        json = response.json()
        version = SpigetVersion.from_timestamp(
            name=json["name"], date=json["releaseDate"], version_id=json["id"],
        )
        return version

    def download_url(self, version: SpigetVersion) -> str:
        return f"{self._base_url}/resources/{self._resource}/versions/{version.version_id}/download"
