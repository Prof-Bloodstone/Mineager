from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Union
from zipfile import ZipFile

import yaml
from requests import Session

from mineager import utils


class Version:
    def __init__(self, name: str, version: str, date: datetime):
        self.name = name
        self.version = version
        self.date = date

    @classmethod
    def from_timestamp(cls, name: str, version: str, date: int, *args, **kwargs):
        return cls(name, version, datetime.fromtimestamp(date), *args, **kwargs)

    def as_tuple(self) -> tuple:
        return self.name, self.version, self.date

    def __str__(self) -> str:
        return f"{type(self).__name__}(name={self.name},version={self.version},date={self.date})"

    @staticmethod
    def __is_valid_operand(other):
        required_attributes = (
            "name",
            "version",
        )
        return all(hasattr(other, attribute) for attribute in required_attributes)

    def __eq__(self, other):
        if not self.__is_valid_operand(other):
            return NotImplemented
        return (self.name, self.version) == (other.name, other.version)

    def __lt__(self, other):
        if not self.__is_valid_operand(other):
            return NotImplemented
        if self.name != other.name:
            return NotImplemented
        if not hasattr(other, "date"):
            return NotImplemented
        # TODO: Compare versions if they are SEMVER?
        return self.date < other.date


class Plugin(ABC):

    type: str = NotImplemented
    _session: Session = Session()

    def __init__(self, name, resource):
        self._name = name
        self._resource = resource
        self.__latest_version = None

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(name={self._name!r}, resource={self._resource!r})"
        )

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
    def name(self):
        return self._name

    @property
    def resource(self):
        return self._resource

    @property
    def latest_version(self):
        if self.__latest_version is None:
            self.__latest_version = self.get_latest_version_info()
        return self.__latest_version

    def version_from_file(self, file: Path = None) -> Union[Version, None]:
        if file is None:
            file = self.default_file_path
        if not file.exists():
            return None

        with ZipFile(file) as zipfile:
            try:
                zipfile.getinfo("plugin.yml")
            except KeyError as e:
                raise NotAPluginException(f"{file} does not contain plugin.yml!") from e
            # date = datetime(*zipinfo.date_time)

            with zipfile.open("plugin.yml") as plug:
                data = yaml.safe_load(plug)
            version = data["version"]
            return Version.from_timestamp(
                name=file.stem, version=version, date=int(file.stat().st_mtime)
            )

    def _download(self, version: Version, file: Path) -> None:
        url = self.download_url(version)
        response = self._get(url)
        if not response.ok and response.headers.get("server") == "cloudflare":
            raise ManualDownloadRequired("Cloudflare blocked automatic download.", url)
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
    def __init__(self, msg: str, url: str):
        self._raw_msg = msg
        self.url = url
        self._msg = f"{msg} {url}"
        super().__init__(self._msg)


class NotAPluginException(Exception):
    pass
