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
from inspect import getfullargspec
from pathlib import Path
from typing import Any, Callable, Iterable

from requests import Response


def get_function_kwargs(fun: Callable[..., Any]) -> Iterable[str]:
    """Extract function arguments from callable."""
    # Potentially should use inspect.signature
    if {"args", "keywords", "func"}.issubset(dir(fun)):
        # assume a partial object
        spec = getfullargspec(fun.func).args[len(fun.args) :]
        return [var for var in spec if var not in fun.keywords]
    if getattr(fun, "__self__", None) is not None:
        # bound method
        return getfullargspec(fun).args[1:]
    return getfullargspec(fun).args


# Standard difflib could be used for more thorough approach: https://stackoverflow.com/a/39404777
# Unfortunately it's known to have many bugs
# Another one would be to instead use Levenshtein distance,
# But the only python lib is outdated, and has installation issues
def common_start_substring(sa, sb):
    """Return the longest common substring from the beginning of sa and sb"""

    def _iter():
        for a, b in zip(sa, sb):
            if a == b:
                yield a
            else:
                return

    return "".join(_iter())


def response_to_file(response: Response, file: Path) -> None:
    """Writes requests.Response content to file."""
    with file.open("wb") as f:
        for chunk in response.iter_content():
            f.write(chunk)
