from pathlib import Path

from requests import Response


def response_to_file(response: Response, file: Path) -> None:
    with file.open("wb") as f:
        for chunk in response.iter_content():
            f.write(chunk)
