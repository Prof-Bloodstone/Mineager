from .Plugin import Plugin, Version
from datetime import datetime


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
