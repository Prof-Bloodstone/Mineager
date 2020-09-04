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
import os
import re
from typing import Callable, List
from urllib.parse import urlparse

from mineager.globals import SESSION
from mineager.plugins import GithubPlugin, JenkinsPlugin, Plugin, SpigetPlugin


class UrlParser:
    _spigot_regexp = re.compile(
        r"^/resources/(?P<name>[-a-zA-Z]+)(?:-\d[\w-]*)?\.(?P<resource>\d+)/"
    )
    _github_regexp = re.compile(r"^/(?P<resource>[-\w]+/(?P<name>\w+))")
    _jenkins_regexp = re.compile(
        r"^(?P<sub_url>(?:/job/[^/]+)+)/(?P<build>\d+)(?P<path>/artifact/(?P<jar_name>.+\.jar$))"
    )

    _name_regexp = re.compile("^(?P<name>[-a-zA-Z_]+[a-zA-Z])")

    _session = SESSION

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
        url = url if urlparse(url).netloc != "" else f"http://{url}"
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
            raise UrlParsingException(
                f"Unable to extract plugin info from {parsed_url.path} - full url: {url}"
            )
        name = match["name"]
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
            raise UrlParsingException(
                f"Unable to extract plugin info from {parsed_url.path} - full url: {url}"
            )
        name = match["name"]
        resource = match["resource"]
        return GithubPlugin(name, resource)

    @classmethod
    def _parse_jenkins(cls, url: str) -> JenkinsPlugin:
        """Parse plugin info from Jenkins URL

            Example usage:
                >>> UrlParser._parse_jenkins('https://ci.lucko.me/job/LuckPerms/1155/artifact/bukkit/build/libs/LuckPerms-Bukkit-5.1.98.jar')
                JenkinsPlugin(name='Luckperms-Bukkit', resource='bukkit/build/libs/LuckPerms-Bukkit-5.1.98.jar', url='https://ci.lucko.me/job/LuckPerms')
                >>> UrlParser._parse_jenkins('https://example.com')
                Traceback (most recent call last):
                    ...
                mineager.UrlParser.InvalidUrlForParser: Could not find jenkins header in response from https://example.com
                >>> UrlParser._parse_jenkins('https://ci.lucko.me/job/LuckPerms/1155/')
                Traceback (most recent call last):
                    ...
                mineager.UrlParser.UrlParsingException: Unable to extract plugin info from /job/LuckPerms/1155/ - full url: https://ci.lucko.me/job/LuckPerms/1155/.

        """
        parsed_url = urlparse(url)
        base_url = parsed_url._replace(path="").geturl()
        req = cls._session.get(base_url)
        if "x-jenkins" not in req.headers:
            raise InvalidUrlForParser(
                f"Could not find jenkins header in response from {base_url}"
            )
        match = cls._jenkins_regexp.match(parsed_url.path)
        if not match:
            raise UrlParsingException(
                f"Unable to extract plugin info from {parsed_url.path} - full url: {url}."
            )
        resource = match["jar_name"]
        name_match = cls._name_regexp.match(os.path.basename(resource))
        name = name_match["name"] if name_match else resource
        job_url = parsed_url._replace(path=match["sub_url"]).geturl()
        return JenkinsPlugin(name, resource, job_url)


class InvalidUrlForParser(Exception):
    pass


class UrlParsingException(Exception):
    pass


class NotImplementedUrlParserException(NotImplementedError):
    pass
