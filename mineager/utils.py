from requests import Response
from pathlib import Path


def response_to_file(response: Response, file: Path) -> None:
    print(f"Writing to {file}") # TODO: remove
    with file.open("wb") as f:
        for chunk in response.iter_content():
            f.write(chunk)
