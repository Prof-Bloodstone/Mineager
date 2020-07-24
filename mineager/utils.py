from requests import Response
from pathlib import Path


from enum import Enum


def response_to_file(response: Response, file: Path) -> None:
    with file.open("wb") as f:
        for chunk in response.iter_content():
            f.write(chunk)


class CLIColors(Enum):
    # TODO: Decide on colors
    UP_TO_DATE = "green"
    NEW = "yellow"
    UPDATE_AVAILABLE = "red"
