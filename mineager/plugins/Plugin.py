from abc import ABC, abstractmethod
from datetime import datetime

from requests import Session
from pathlib import Path
from mineager import utils

from zipfile import ZipFile

import yaml


class Version:
    def __init__(self, name: str, version: str, date: datetime):
        self.name = name
        self.version = version
        self.date = date

    @classmethod
    def from_timestamp(cls, name: str, version: str, date: int, *args, **kwargs):
        return cls(name, version, datetime.fromtimestamp(date), *args, **kwargs)

    def __str__(self) -> str:
        return f"{type(self).__name__}(name={self.name},version={self.version},date={self.date})"


class Plugin(ABC):

    def __init__(self, name, resource, session: Session = Session()):
        self._name = name
        self._resource = resource
        self._session = session
        self.clear_cache()

    def __repr__(self) -> str:
        return f"{type(self).__name__}(name={self._name!r}, resource={self._resource!r})"

    def clear_cache(self):
        self.__latest_version = None

    def _get(self, url: str, *args, **kwargs):
        return self._session.get(url, *args, **kwargs)

    @property
    def default_file_path(self) -> Path:
        return Path(f'./plugins/{self._name.replace(" ", "_")}.jar')

    @abstractmethod
    def get_latest_version_info(self) -> Version:
        pass

    @property
    def latest_version(self):
        if self.__latest_version is None:
            self.__latest_version = self.get_latest_version_info()
        return self.__latest_version

    def version_from_file(self, file: Path = None) -> Version:
        if file is None:
            file = self.default_file_path
        if not file.exists():
            print(f"Nonexistent: {file}")
            return None  # TODO: Throw an error

        with ZipFile(file) as zipfile:
            try:
                zipinfo = zipfile.getinfo('plugin.yml')
            except KeyError as e:
                raise NotAPluginException(f"{file} does not contain plugin.yml!") from e
            # date = datetime(*zipinfo.date_time)

            with zipfile.open('plugin.yml') as plug:
                data = yaml.safe_load(plug)
            version = data['version']
            return Version.from_timestamp(name=file.stem, version=version, date=int(file.stat().st_mtime))

    def _download(self, version: Version, file: Path) -> None:
        response = self._get(self.download_url(version))
        response.raise_for_status()
        utils.response_to_file(response, file)

    def download(self, version: Version = None, file: Path = None) -> None:
        if version is None:
            version = self.latest_version
        if file is None:
            file = self.default_file_path
        self._download(version, file)

    @abstractmethod
    def download_url(self, version: Version) -> str:
        pass


class ManualDownloadRequired(Exception):
    pass


class NotAPluginException(Exception):
    pass
