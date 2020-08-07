import re
from typing import Callable, List
from urllib.parse import urlparse

from .plugins import GithubPlugin, Plugin, SpigetPlugin


class UrlParser:
    _spigot_regexp = re.compile(
        r"^/resources/(?P<name>[-a-zA-Z]+)(?:-\d[\w-]*)\.(?P<resource>\d+)/"
    )
    _github_regexp = re.compile(r"^/(?P<resource>[-\w]+/(?P<name>\w+))")

    @classmethod
    def _get_parsers(cls) -> List[Callable]:
        """Get all methods that start with `_parse_`"""
        return [
            attr
            for attr in [
                getattr(cls, func) for func in dir(cls) if func.startswith("_parse_")
            ]
            if callable(attr)
        ]

    @classmethod
    def parse(cls, url: str) -> Plugin:
        """Tries to extract plugin type from URL"""
        url = url if urlparse(url).netloc != "" else f"//{url}"
        for parser in cls._get_parsers():
            try:
                return parser(url)
            except InvalidUrlForParser:
                pass  # Try another parser
        raise NotImplementedUrlParserException(
            f"Unable to parse '{url}' using any of the existing parsers!"
        )

    @classmethod
    def _parse_spigot(cls, url: str) -> SpigetPlugin:
        parsed_url = urlparse(url)
        if "spigotmc.org" not in parsed_url.netloc:
            raise InvalidUrlForParser(
                f"'spigotmc.org' is not in {parsed_url.netloc} - from {url}"
            )
        match = cls._spigot_regexp.match(parsed_url.path)
        if not match:
            UrlParsingException(
                f"Unable to extract plugin info from {parsed_url.path} - full url: {url}"
            )
        name = match["name"].replace("-", " ").title()
        resource = match["resource"]
        return SpigetPlugin(name, resource)

    @classmethod
    def _parse_github(cls, url: str) -> GithubPlugin:
        parsed_url = urlparse(url)
        if "github.com" not in parsed_url.netloc:
            raise InvalidUrlForParser(
                f"'github.com' is not in {parsed_url.netloc} - from {url}"
            )
        match = cls._github_regexp.match(parsed_url.path)
        if not match:
            UrlParsingException(
                f"Unable to extract plugin info from {parsed_url.path} - full url: {url}"
            )
        name = match["name"].replace("-", " ").title()
        resource = match["resource"]
        return GithubPlugin(name, resource)


class InvalidUrlForParser(Exception):
    pass


class UrlParsingException(Exception):
    pass


class NotImplementedUrlParserException(NotImplementedError):
    pass
